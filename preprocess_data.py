"""
Script de processamento e estruturação dos dados educacionais.
Lê a planilha consolidada 'planilha ref/divulgacao_pr_consolidado.xlsx',
classifica as escolas de acordo com as diretrizes do projeto e mapeamento KML,
associa coordenadas geográficas e converte os dados para formatos analíticos (wide e long),
gerando artefatos otimizados em Parquet para carregamento ultrarrápido no painel.
"""

import re
import unicodedata
from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
PLANILHA_PATH = BASE_DIR / "planilha ref" / "divulgacao_pr_consolidado.xlsx"
MAP_CM_PATH = BASE_DIR / "data" / "mapeamento_escolas_civico_militares.csv"
MUN_PATH = BASE_DIR / "data" / "municipios_pr.csv"
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# 1. Carrega coordenadas dos municípios do PR
df_mun = pd.read_csv(MUN_PATH) if MUN_PATH.exists() else pd.DataFrame()
def norm_mun(nome: str) -> str:
    if not isinstance(nome, str): return ""
    nome = unicodedata.normalize("NFKD", nome).encode("ASCII", "ignore").decode("ASCII").upper()
    return re.sub(r"[^A-Z0-9\s]", "", nome).strip()

mun_coords = {}
if not df_mun.empty:
    df_mun["NORM_MUN"] = df_mun["nome"].apply(norm_mun)
    mun_coords = df_mun.set_index("NORM_MUN")[["latitude", "longitude"]].to_dict(orient="index")

# 2. Carrega mapeamento auditado de escolas cívico-militares com KML
IDS_CIVICO_MILITARES = set()
KML_COORDS = {} # id_escola -> (lat, lon)

if MAP_CM_PATH.exists():
    df_map = pd.read_csv(MAP_CM_PATH, sep=";", encoding="utf-8-sig")
    for _, row in df_map.iterrows():
        try:
            if pd.notna(row["ID_ESCOLA"]):
                id_e = int(row["ID_ESCOLA"])
                IDS_CIVICO_MILITARES.add(id_e)
                if pd.notna(row.get("LATITUDE")) and pd.notna(row.get("LONGITUDE")):
                    KML_COORDS[id_e] = (float(row["LATITUDE"]), float(row["LONGITUDE"]))
        except (ValueError, TypeError):
            continue

print(f"Mapeamento carregado: {len(IDS_CIVICO_MILITARES)} escolas cívico-militares com {len(KML_COORDS)} coordenadas exatas.")

def classificar_tipo_gestao(id_escola: int, nome: str) -> str:
    # 1. Verifica se o ID_ESCOLA está no mapeamento oficial auditado do KML
    try:
        if int(id_escola) in IDS_CIVICO_MILITARES:
            return "Cívico-Militar"
    except (ValueError, TypeError):
        pass
        
    nome_str = str(nome).strip().upper()
    # Exclusão explícita de CMEI
    if re.search(r'C\s*M\s*E\s*I', nome_str):
        return "Não Cívico-Militar"
    
    # 2. Verifica siglas oficiais da SEED-PR e INEP
    padrao_cm = r'(\bC\s*E\s*CM\b|\bE\s*E\s*CM\b|\bE\s*M\s*CM\b|\bE\s*C\s*M\b|\bCMEF\b|\bCPM\b|\bC\.P\.M\b|\bC\.M\b|CIVIC|MILITAR)'
    if re.search(padrao_cm, nome_str):
        return "Cívico-Militar"
        
    return "Não Cívico-Militar"


ETAPAS = {
    "divulgacao_anos_iniciais": "Anos Iniciais (1º-5º)",
    "divulgacao_anos_finais": "Anos Finais (6º-9º)",
    "divulgacao_ensino_medio": "Ensino Médio",
}

def processar_dados():
    print(f"Lendo planilha: {PLANILHA_PATH}")
    xls = pd.ExcelFile(PLANILHA_PATH)
    
    dfs_tidy = []
    dfs_wide = []
    
    for sheet_name, etapa_label in ETAPAS.items():
        print(f"Processando etapa: {etapa_label} (aba: {sheet_name})")
        df_raw = pd.read_excel(xls, sheet_name=sheet_name)
        
        # Filtro estrito: apenas Estado do Paraná
        if "SG_UF" in df_raw.columns:
            df_raw = df_raw[df_raw["SG_UF"] == "PR"].copy()
            
        df_raw["ETAPA"] = etapa_label
        df_raw["TIPO_GESTAO"] = df_raw.apply(
            lambda r: classificar_tipo_gestao(r["ID_ESCOLA"], r["NO_ESCOLA"]), axis=1
        )
        
        # Coordenadas geográficas
        def extrair_lat(row):
            id_e = row["ID_ESCOLA"]
            if id_e in KML_COORDS:
                return KML_COORDS[id_e][0]
            mun = norm_mun(row.get("NO_MUNICIPIO", ""))
            return mun_coords.get(mun, {}).get("latitude", np.nan)

        def extrair_lon(row):
            id_e = row["ID_ESCOLA"]
            if id_e in KML_COORDS:
                return KML_COORDS[id_e][1]
            mun = norm_mun(row.get("NO_MUNICIPIO", ""))
            return mun_coords.get(mun, {}).get("longitude", np.nan)

        df_raw["LATITUDE"] = df_raw.apply(extrair_lat, axis=1)
        df_raw["LONGITUDE"] = df_raw.apply(extrair_lon, axis=1)
        df_raw["COORDENADA_TIPO"] = df_raw["ID_ESCOLA"].map(
            lambda x: "EXATA_KML" if x in KML_COORDS else "CENTROIDE_MUNICIPIO"
        )
        
        # Converte colunas de valores para numérico float
        for c in df_raw.columns:
            if c.startswith("VL_"):
                df_raw[c] = pd.to_numeric(df_raw[c], errors="coerce")
                
        dfs_wide.append(df_raw.copy())
        
        # Anos disponíveis
        cols = df_raw.columns
        anos = sorted(list(set([re.search(r'\d{4}', c).group() for c in cols if re.search(r'\d{4}', c)])))
        
        for ano in anos:
            col_mat = f"VL_NOTA_MATEMATICA_{ano}"
            col_port = f"VL_NOTA_PORTUGUES_{ano}"
            col_media = f"VL_NOTA_MEDIA_{ano}"
            col_ideb = f"VL_OBSERVADO_{ano}"
            col_proj = f"VL_PROJECAO_{ano}"
            col_rend = f"VL_INDICADOR_REND_{ano}"
            col_aprov = f"VL_APROVACAO_{ano}_SI_4"
            
            sub = pd.DataFrame({
                "SG_UF": df_raw["SG_UF"],
                "CO_MUNICIPIO": df_raw["CO_MUNICIPIO"],
                "NO_MUNICIPIO": df_raw["NO_MUNICIPIO"],
                "ID_ESCOLA": df_raw["ID_ESCOLA"],
                "NO_ESCOLA": df_raw["NO_ESCOLA"],
                "REDE": df_raw["REDE"],
                "ETAPA": etapa_label,
                "TIPO_GESTAO": df_raw["TIPO_GESTAO"],
                "LATITUDE": df_raw["LATITUDE"],
                "LONGITUDE": df_raw["LONGITUDE"],
                "COORDENADA_TIPO": df_raw["COORDENADA_TIPO"],
                "ANO": int(ano),
                "SAEB_MATEMATICA": df_raw[col_mat] if col_mat in cols else np.nan,
                "SAEB_PORTUGUES": df_raw[col_port] if col_port in cols else np.nan,
                "SAEB_NOTA_MEDIA": df_raw[col_media] if col_media in cols else np.nan,
                "IDEB_OBSERVADO": df_raw[col_ideb] if col_ideb in cols else np.nan,
                "IDEB_PROJECAO": df_raw[col_proj] if col_proj in cols else np.nan,
                "INDICADOR_RENDIMENTO": df_raw[col_rend] if col_rend in cols else np.nan,
                "TAXA_APROVACAO": df_raw[col_aprov] if col_aprov in cols else np.nan,
            })
            dfs_tidy.append(sub)
            
    df_tidy_all = pd.concat(dfs_tidy, ignore_index=True)
    df_tidy_all.to_parquet(DATA_DIR / "escolas_tidy.parquet", index=False)
    print(f"Salvo: {DATA_DIR / 'escolas_tidy.parquet'} (Total de registros analíticos: {len(df_tidy_all)})")
    
    # Salva wide por etapa
    for sheet_name, df_w in zip(ETAPAS.keys(), dfs_wide):
        etapa_slug = sheet_name.replace("divulgacao_", "")
        df_w.to_parquet(DATA_DIR / f"escolas_wide_{etapa_slug}.parquet", index=False)
        print(f"Salvo wide para {etapa_slug}: {len(df_w)} linhas.")
        
    print("Processamento concluído com sucesso!")

if __name__ == "__main__":
    processar_dados()
