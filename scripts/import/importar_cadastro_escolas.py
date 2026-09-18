#!/usr/bin/env python3
"""
importar_cadastro_escolas.py

Script para leitura, extração e consolidação dos dados cadastrais oficiais
das escolas públicas do Paraná a partir das fontes primárias locais:
1. INEP / Censo Escolar da Educação Básica 2023 (tx_rend_escolas_2023.xlsx);
2. SEED/PR / Editais Oficiais 2020-2025 (editais de consulta pública, criação e expansão CCM);
3. SEED/PR / Mapeamento Georreferenciado Oficial (KML de colégios cívico-militares);
4. IBGE / Cadastro Oficial de Municípios do Paraná (coordenadas e códigos IBGE).

Saídas intermediárias / raw consolidadas em memória para o transformador.
"""

from pathlib import Path
import re
import unicodedata
import pandas as pd
import numpy as np

def normalizar_texto(texto):
    if not isinstance(texto, str):
        return ""
    texto = unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("ASCII").upper()
    return re.sub(r"[^A-Z0-9\s]", " ", texto).strip()

def carregar_dados_censo(raw_rend_path: Path) -> pd.DataFrame:
    print(f"1. Lendo microdados do Censo Escolar 2023: {raw_rend_path.name}...")
    df_raw = pd.read_excel(raw_rend_path, skiprows=8, engine="calamine")
    
    # Filtrar Paraná (coluna 2: SG_UF)
    uf_col = df_raw.columns[2]
    df_pr = df_raw[df_raw[uf_col] == "PR"].copy()
    print(f"   Total de estabelecimentos do Paraná localizados: {len(df_pr)}")
    
    # Extração das colunas cadastrais principais
    # 0: NU_ANO_CENSO, 2: SG_UF, 3: CO_MUNICIPIO, 4: NO_MUNICIPIO, 5: CO_ENTIDADE, 6: NO_ENTIDADE, 7: NO_CATEGORIA, 8: NO_DEPENDENCIA
    # 10: 1_CAT_FUN_AI, 11: 1_CAT_FUN_AF, 21: 1_CAT_MED
    df_censo = pd.DataFrame({
        "codigo_inep": pd.to_numeric(df_pr.iloc[:, 5], errors="coerce").astype("Int64"),
        "nome_escola_censo": df_pr.iloc[:, 6].astype(str).str.strip(),
        "codigo_ibge_municipio": pd.to_numeric(df_pr.iloc[:, 3], errors="coerce").astype("Int64"),
        "municipio_censo": df_pr.iloc[:, 4].astype(str).str.strip(),
        "uf": "PR",
        "localizacao": df_pr.iloc[:, 7].astype(str).str.strip(), # Urbana / Rural
        "dependencia_administrativa": df_pr.iloc[:, 8].astype(str).str.strip(), # Estadual / Municipal / Federal / Privada
        "cat_fun_ai": df_pr.iloc[:, 10].astype(str),
        "cat_fun_af": df_pr.iloc[:, 11].astype(str),
        "cat_med": df_pr.iloc[:, 21].astype(str),
        "ano_censo": int(df_pr.iloc[0, 0])
    })
    
    # Deduplicar por código INEP
    df_censo = df_censo.dropna(subset=["codigo_inep"]).drop_duplicates(subset=["codigo_inep"])
    print(f"   Total de escolas únicas cadastradas no Censo 2023: {len(df_censo)}")
    return df_censo

def extrair_nre_editais(editais_dir: Path, codigos_alvo: set) -> dict:
    print(f"2. Extraindo Núcleos Regionais de Educação (NRE) dos editais em {editais_dir}...")
    map_nre = {}
    map_nome_edital = {}
    
    # Ordenar editais cronologicamente
    txt_files = sorted(editais_dir.glob("*.txt"))
    for txt_file in txt_files:
        with open(txt_file, encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        # Padrão 1: COD NRE MUN ESTABELECIMENTO (Ex: Edital 101/2023, 107/2023, etc.)
        matches1 = re.findall(r"(\d{8})\s+([A-ZÀ-Ú\.\s]{3,25})\s+([A-ZÀ-Ú\.\s]{3,30})\s+([^\n\r]+)", content)
        for m in matches1:
            cod = int(m[0])
            nre = m[1].strip()
            est = m[3].strip()
            if cod in codigos_alvo and cod not in map_nre:
                # Sanitizar NRE
                nre_clean = re.sub(r"^(NRE|N\.R\.E\.)\s*", "", nre, flags=re.IGNORECASE).strip()
                map_nre[cod] = nre_clean
                map_nome_edital[cod] = est

        # Padrão 2: CÓDIGO NRE MUNICÍPIO (Ex: Edital 125/2025 e 136/2025)
        matches2 = re.findall(r"(\d{8})\s+([A-ZÀ-Ú\.\s]{3,20})\s+([A-ZÀ-Ú\.\s]{3,25})\s+([^\n\r]+)", content)
        for m in matches2:
            cod = int(m[0])
            nre = m[1].strip()
            est = m[3].strip()
            if cod in codigos_alvo and cod not in map_nre:
                nre_clean = re.sub(r"^(NRE|N\.R\.E\.)\s*", "", nre, flags=re.IGNORECASE).strip()
                map_nre[cod] = nre_clean
                if cod not in map_nome_edital:
                    map_nome_edital[cod] = est

    print(f"   NREs identificados nos editais: {len(map_nre)} de {len(codigos_alvo)} escolas alvo")
    return map_nre, map_nome_edital

def carregar_coordenadas_kml(kml_map_path: Path) -> dict:
    print(f"3. Lendo coordenadas georreferenciadas do mapeamento KML: {kml_map_path.name}...")
    df_map = pd.read_csv(kml_map_path, sep=";")
    coords = {}
    for _, r in df_map.iterrows():
        id_e = int(r["ID_ESCOLA"])
        lat = float(r["LATITUDE"])
        lon = float(r["LONGITUDE"])
        nome_kml = str(r["NOME_KML"]).strip()
        coords[id_e] = {
            "latitude": lat,
            "longitude": lon,
            "tipo_coordenada": "EXATA_KML",
            "nome_kml": nome_kml
        }
    print(f"   Escolas com coordenadas exatas KML: {len(coords)}")
    return coords

def carregar_centroides_municipios(mun_path: Path) -> dict:
    print(f"4. Lendo centroides municipais IBGE: {mun_path.name}...")
    df_mun = pd.read_csv(mun_path)
    mun_coords = {}
    for _, r in df_mun.iterrows():
        co_ibge = int(r["codigo_ibge"])
        nome_mun = str(r["nome"]).strip().upper()
        lat = float(r["latitude"])
        lon = float(r["longitude"])
        mun_coords[co_ibge] = {"latitude": lat, "longitude": lon, "nome": nome_mun}
        # Também mapear por nome normalizado
        norm_nome = normalizar_texto(nome_mun)
        mun_coords[norm_nome] = {"latitude": lat, "longitude": lon, "codigo_ibge": co_ibge}
    return mun_coords

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent.parent
    raw_rend = base_dir / "data" / "raw" / "rendimento" / "tx_rend_escolas_2023" / "tx_rend_escolas_2023.xlsx"
    editais_dir = base_dir / "data" / "extracted" / "editais"
    kml_map = base_dir / "data" / "mapeamento_escolas_civico_militares.csv"
    mun_csv = base_dir / "data" / "municipios_pr.csv"
    
    # Carregar lista de 201 escolas auditadas
    hist_ccm = pd.read_csv(base_dir / "data" / "processed" / "historico_ccm_por_ano.csv", sep=";")
    codigos_201 = set(hist_ccm["codigo_inep"].unique())
    
    df_censo = carregar_dados_censo(raw_rend)
    map_nre, map_nome_edital = extrair_nre_editais(editais_dir, codigos_201)
    coords_kml = carregar_coordenadas_kml(kml_map)
    mun_coords = carregar_centroides_municipios(mun_csv)
    print("Importação e leitura preliminar concluída com sucesso!")
