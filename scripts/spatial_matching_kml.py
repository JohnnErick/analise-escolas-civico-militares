"""
Script de Validação Espacial e Matching de Escolas Cívico-Militares
Cruza os 306 pontos georreferenciados do arquivo KML com a base oficial do INEP e
coordenadas municipais do IBGE, eliminando ambiguidades e falsos positivos.
"""

import xml.etree.ElementTree as ET
import unicodedata
import re
from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
KML_PATH = BASE_DIR / "planilha ref" / "Colégios Cívico-Militares do Paraná.kml"
MUN_PATH = BASE_DIR / "data" / "municipios_pr.csv"
INEP_PARQUET = BASE_DIR / "data" / "escolas_tidy.parquet"
OUTPUT_MAP_CSV = BASE_DIR / "data" / "mapeamento_escolas_civico_militares.csv"

# Stopwords escolares para normalização de nomes
STOPWORDS = {
    "COLEGIO", "ESTADUAL", "CIVICO", "MILITAR", "CIVICOMILITAR", "ENSINO", "FUNDAMENTAL",
    "MEDIO", "EF", "EM", "PROFISSIONAL", "PROFIS", "PE", "PROF", "PROFA", "DR", "CE", 
    "C", "E", "M", "P", "EE", "DE", "DA", "DO", "DOS", "DAS", "EEM", "CECM", "CPM"
}

def normalizar_texto(texto: str) -> str:
    if not isinstance(texto, str):
        return ""
    # Remove acentos
    texto = unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("ASCII").upper()
    # Remove pontuações e caracteres especiais
    texto = re.sub(r"[^A-Z0-9\s]", " ", texto)
    tokens = [w for w in texto.split() if w not in STOPWORDS and len(w) > 1]
    return " ".join(tokens)

def normalizar_municipio(nome: str) -> str:
    if not isinstance(nome, str):
        return ""
    nome = unicodedata.normalize("NFKD", nome).encode("ASCII", "ignore").decode("ASCII").upper()
    return re.sub(r"[^A-Z0-9\s]", "", nome).strip()

def executar_matching_espacial():
    print("1. Carregando KML oficial...")
    tree = ET.parse(KML_PATH)
    root = tree.getroot()
    ns = {"kml": "http://www.opengis.net/kml/2.2"}
    placemarks = root.findall(".//kml:Placemark", ns) or root.findall(".//Placemark")
    
    kml_records = []
    for i, pm in enumerate(placemarks):
        name_node = pm.find("kml:name", ns) if pm.find("kml:name", ns) is not None else pm.find("name")
        coords_node = pm.find(".//kml:coordinates", ns) if pm.find(".//kml:coordinates", ns) is not None else pm.find(".//coordinates")
        
        name = name_node.text.strip() if name_node is not None and name_node.text else f"PONTO_{i+1}"
        coords_str = coords_node.text.strip() if coords_node is not None and coords_node.text else "0,0,0"
        parts = coords_str.split(",")
        lon, lat = float(parts[0]), float(parts[1])
        
        kml_records.append({
            "KML_IDX": i,
            "NOME_KML": name,
            "LATITUDE": lat,
            "LONGITUDE": lon,
            "NORM_KML": normalizar_texto(name)
        })
    df_kml = pd.DataFrame(kml_records)
    print(f"   -> {len(df_kml)} pontos carregados do KML.")

    print("2. Carregando coordenadas municipais do Paraná...")
    df_mun = pd.read_csv(MUN_PATH)
    df_mun["NORM_MUN"] = df_mun["nome"].apply(normalizar_municipio)
    mun_dict = df_mun.set_index("NORM_MUN")[["latitude", "longitude", "codigo_ibge", "nome"]].to_dict(orient="index")

    print("3. Carregando escolas estaduais da base oficial do INEP...")
    df_inep = pd.read_parquet(INEP_PARQUET)
    escolas_inep = df_inep[df_inep["REDE"] == "Estadual"][
        ["ID_ESCOLA", "NO_ESCOLA", "NO_MUNICIPIO", "CO_MUNICIPIO"]
    ].drop_duplicates().copy()
    
    escolas_inep["NORM_ESCOLA"] = escolas_inep["NO_ESCOLA"].apply(normalizar_texto)
    escolas_inep["NORM_MUN"] = escolas_inep["NO_MUNICIPIO"].apply(normalizar_municipio)
    
    # Adiciona coordenadas do município à escola
    escolas_inep["MUN_LAT"] = escolas_inep["NORM_MUN"].map(lambda m: mun_dict.get(m, {}).get("latitude", np.nan))
    escolas_inep["MUN_LON"] = escolas_inep["NORM_MUN"].map(lambda m: mun_dict.get(m, {}).get("longitude", np.nan))

    print("4. Executando matching geoespacial multi-critério...")
    resultados = []
    
    # Casos manuais conhecidos onde o nome no KML era endereço físico ou divergência histórica
    OVERRIDE_MANUAL = {
        "R. Rudolf Keilhold, 173": 41032446, # Col. Est. Profª Olympia Morais de Tormenta - Londrina
    }
    
    for _, kml_row in df_kml.iterrows():
        nome_kml = kml_row["NOME_KML"]
        lat_k = kml_row["LATITUDE"]
        lon_k = kml_row["LONGITUDE"]
        norm_k = kml_row["NORM_KML"]
        k_tokens = set(norm_k.split())

        # Caso com override manual
        if nome_kml in OVERRIDE_MANUAL:
            target_id = OVERRIDE_MANUAL[nome_kml]
            match_row = escolas_inep[escolas_inep["ID_ESCOLA"] == target_id].iloc[0]
            resultados.append({
                "NOME_KML": nome_kml,
                "ID_ESCOLA": int(target_id),
                "NO_ESCOLA_INEP": match_row["NO_ESCOLA"],
                "NO_MUNICIPIO": match_row["NO_MUNICIPIO"],
                "CO_MUNICIPIO": match_row["CO_MUNICIPIO"],
                "LATITUDE": lat_k,
                "LONGITUDE": lon_k,
                "DISTANCIA_KM": 0.0,
                "MATCH_TYPE": "OVERRIDE_ENDERECO",
                "SCORE": 1.0
            })
            continue

        # Calcula distância aproximada em km para todas as escolas estaduais
        dlat = (escolas_inep["MUN_LAT"] - lat_k) * 110.57
        dlon = (escolas_inep["MUN_LON"] - lon_k) * 101.44
        dist_km = np.hypot(dlat, dlon)

        # Filtra preferencialmente escolas num raio de até 45km
        # Se nenhuma bater, expande para o estado
        candidatos = escolas_inep[dist_km <= 45.0].copy()
        candidatos["DIST_KM"] = dist_km[dist_km <= 45.0]
        
        # Se vazio (por exemplo área de fronteira), avalia todas as escolas
        if candidatos.empty:
            candidatos = escolas_inep.copy()
            candidatos["DIST_KM"] = dist_km

        melhor_candidato = None
        maior_pontuacao = -9999.0

        for _, cand in candidatos.iterrows():
            cand_tokens = set(cand["NORM_ESCOLA"].split())
            inter = k_tokens.intersection(cand_tokens)
            n_inter = len(inter)
            
            # Similaridade de Jaccard dos tokens significativos
            union_len = len(k_tokens.union(cand_tokens))
            jaccard = (n_inter / union_len) if union_len > 0 else 0
            
            # Penalidade proporcional à distância da sede municipal (0.01 por km)
            d = cand["DIST_KM"]
            score = (n_inter * 2.0) + (jaccard * 3.0) - (d * 0.03)
            
            # Bônus especial se o nome do município estiver mencionado no nome KML
            if cand["NORM_MUN"] in norm_k:
                score += 1.5

            if score > maior_pontuacao:
                maior_pontuacao = score
                melhor_candidato = (cand, d, n_inter, jaccard)

        if melhor_candidato is not None and melhor_candidato[2] > 0:
            cand, d, n_inter, jaccard = melhor_candidato
            m_type = "EXATO_LOCALIZADO" if n_inter >= 2 and d <= 25.0 else "CONFIRMADO_GEO"
            resultados.append({
                "NOME_KML": nome_kml,
                "ID_ESCOLA": int(cand["ID_ESCOLA"]),
                "NO_ESCOLA_INEP": cand["NO_ESCOLA"],
                "NO_MUNICIPIO": cand["NO_MUNICIPIO"],
                "CO_MUNICIPIO": cand["CO_MUNICIPIO"],
                "LATITUDE": lat_k,
                "LONGITUDE": lon_k,
                "DISTANCIA_KM": round(d, 1),
                "MATCH_TYPE": m_type,
                "SCORE": round(maior_pontuacao, 2)
            })
        else:
            # Fallback buscando pelo estado inteiro
            melhor_geral = None
            maior_geral_score = -999
            for _, cand in escolas_inep.iterrows():
                cand_tokens = set(cand["NORM_ESCOLA"].split())
                inter = k_tokens.intersection(cand_tokens)
                if len(inter) > maior_geral_score:
                    maior_geral_score = len(inter)
                    melhor_geral = cand
            
            if melhor_geral is not None and maior_geral_score > 0:
                resultados.append({
                    "NOME_KML": nome_kml,
                    "ID_ESCOLA": int(melhor_geral["ID_ESCOLA"]),
                    "NO_ESCOLA_INEP": melhor_geral["NO_ESCOLA"],
                    "NO_MUNICIPIO": melhor_geral["NO_MUNICIPIO"],
                    "CO_MUNICIPIO": melhor_geral["CO_MUNICIPIO"],
                    "LATITUDE": lat_k,
                    "LONGITUDE": lon_k,
                    "DISTANCIA_KM": round(float(dist_km.loc[melhor_geral.name]), 1),
                    "MATCH_TYPE": "FALLBACK_ESTADUAL",
                    "SCORE": float(maior_geral_score)
                })
            else:
                resultados.append({
                    "NOME_KML": nome_kml,
                    "ID_ESCOLA": None,
                    "NO_ESCOLA_INEP": None,
                    "NO_MUNICIPIO": None,
                    "CO_MUNICIPIO": None,
                    "LATITUDE": lat_k,
                    "LONGITUDE": lon_k,
                    "DISTANCIA_KM": None,
                    "MATCH_TYPE": "NAO_ENCONTRADO",
                    "SCORE": 0.0
                })

    df_final = pd.DataFrame(resultados)
    
    # Salva mapeamento final em CSV delimitado por ponto-e-vírgula
    df_final.to_csv(OUTPUT_MAP_CSV, sep=";", index=False, encoding="utf-8-sig")
    print(f"\n5. Mapeamento final gravado com sucesso em: {OUTPUT_MAP_CSV}")
    print("\n--- Estatísticas do Matching Geoespacial ---")
    print(df_final["MATCH_TYPE"].value_counts())
    print(f"Total de registros KML: {len(df_final)}")
    print(f"Total de ID_ESCOLA únicos identificados: {df_final['ID_ESCOLA'].dropna().nunique()}")
    
    # Exibe amostra dos 5 primeiros
    print("\nPrimeiros 5 registros auditados:")
    print(df_final[["NOME_KML", "NO_ESCOLA_INEP", "NO_MUNICIPIO", "DISTANCIA_KM", "MATCH_TYPE"]].head())

if __name__ == "__main__":
    executar_matching_espacial()
