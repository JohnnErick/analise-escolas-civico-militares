"""
Script de processamento e estruturação dos dados educacionais.
Lê a planilha consolidada 'planilha ref/divulgacao_pr_consolidado.xlsx',
classifica as escolas de acordo com as diretrizes do projeto,
converte os dados para formatos analíticos (wide e long) e
gera artefatos otimizados em Parquet para carregamento ultrarrápido no painel.
"""

import re
from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
PLANILHA_PATH = BASE_DIR / "planilha ref" / "divulgacao_pr_consolidado.xlsx"
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Regra de classificação documentada:
# 1. Identifica escolas cívico-militares com base nas nomenclaturas oficiais da SEED-PR e INEP:
#    - 'C E CM': Colégio Estadual Cívico-Militar
#    - 'E E CM': Escola Estadual Cívico-Militar
#    - 'E M CM': Escola Municipal Cívico-Militar
#    - 'E C M': Escola Cívico-Militar
#    - 'CPM' / 'C.P.M.': Colégio da Polícia Militar
#    - 'CIVICO' / 'CÍVICO' / 'MILITAR'
# 2. Exclui expressamente escolas de educação infantil ('CMEI' / 'C M E I' - Centro Municipal de Educação Infantil)
#    e nomes que possuem apenas 'MILITAR' em outro contexto geográfico sem vínculo militar se houver.
def classificar_tipo_gestao(nome: str) -> str:
    nome_str = str(nome).strip().upper()
    if re.search(r'C\s*M\s*E\s*I', nome_str):
        return "Não Cívico-Militar"
    
    padrao_cm = r'(\bC\s*E\s*CM\b|\bE\s*E\s*CM\b|\bE\s*M\s*CM\b|\bE\s*C\s*M\b|\bCPM\b|\bC\.P\.M\b|\bC\.M\b|CIVIC|MILITAR)'
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
        
        # Colunas cadastrais
        cadastrais = ["SG_UF", "CO_MUNICIPIO", "NO_MUNICIPIO", "ID_ESCOLA", "NO_ESCOLA", "REDE"]
        for col in cadastrais:
            if col not in df_raw.columns:
                print(f"Aviso: coluna {col} ausente na aba {sheet_name}")
                
        df_raw = df_raw.copy()
        df_raw["ETAPA"] = etapa_label
        df_raw["TIPO_GESTAO"] = df_raw["NO_ESCOLA"].apply(classificar_tipo_gestao)
        
        # Converte colunas de valores para numérico float para compatibilidade no Parquet
        for c in df_raw.columns:
            if c.startswith("VL_"):
                df_raw[c] = pd.to_numeric(df_raw[c], errors="coerce")
                
        dfs_wide.append(df_raw.copy())
        
        # Vamos identificar os anos disponíveis para esta etapa
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
    
    # Salva também um wide combinado ou por etapa
    for sheet_name, df_w in zip(ETAPAS.keys(), dfs_wide):
        etapa_slug = sheet_name.replace("divulgacao_", "")
        df_w.to_parquet(DATA_DIR / f"escolas_wide_{etapa_slug}.parquet", index=False)
        print(f"Salvo wide para {etapa_slug}: {len(df_w)} linhas.")
        
    print("Processamento concluído com sucesso!")

if __name__ == "__main__":
    processar_dados()

