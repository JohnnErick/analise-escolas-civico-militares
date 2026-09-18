#!/usr/bin/env python3
"""
importar_ideb_inep.py

Script para leitura, validação e importação das planilhas oficiais de divulgação
do IDEB (Índice de Desenvolvimento da Educação Básica) consolidadas pelo INEP/MEC
para o Estado do Paraná.

Extrai as três etapas de ensino:
- Anos Iniciais do Ensino Fundamental;
- Anos Finais do Ensino Fundamental;
- Ensino Médio.

Fontes:
- data/raw/ideb/divulgacao_pr_consolidado.xlsx (copiado de data/raw/saeb/)

Saídas:
- data/raw/ideb/ideb_anos_iniciais_raw.parquet
- data/raw/ideb/ideb_anos_finais_raw.parquet
- data/raw/ideb/ideb_ensino_medio_raw.parquet
"""

import shutil
from pathlib import Path
import pandas as pd

def run():
    print("=== Iniciando Importação dos Dados Brutos do IDEB (INEP) ===")
    base_dir = Path(__file__).resolve().parent.parent.parent
    raw_ideb_dir = base_dir / "data" / "raw" / "ideb"
    raw_saeb_dir = base_dir / "data" / "raw" / "saeb"
    raw_ideb_dir.mkdir(parents=True, exist_ok=True)

    target_xlsx = raw_ideb_dir / "divulgacao_pr_consolidado.xlsx"
    source_xlsx = raw_saeb_dir / "divulgacao_pr_consolidado.xlsx"

    if not target_xlsx.exists() and source_xlsx.exists():
        print(f"Copiando planilha consolidada oficial para {target_xlsx}...")
        shutil.copy2(source_xlsx, target_xlsx)

    if not target_xlsx.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {target_xlsx}")

    print(f"Lendo planilha oficial do IDEB: {target_xlsx}")
    xl = pd.ExcelFile(target_xlsx)

    sheets = {
        "divulgacao_anos_iniciais": "ideb_anos_iniciais_raw.parquet",
        "divulgacao_anos_finais": "ideb_anos_finais_raw.parquet",
        "divulgacao_ensino_medio": "ideb_ensino_medio_raw.parquet",
    }

    for sheet_name, out_name in sheets.items():
        if sheet_name not in xl.sheet_names:
            print(f"AVISO: Aba '{sheet_name}' não encontrada!")
            continue

        print(f"\nImportando aba '{sheet_name}'...")
        df_sheet = pd.read_excel(xl, sheet_name=sheet_name)
        print(f"  Registros importados: {len(df_sheet)}")

        # Validação de colunas cadastrais
        req_cols = ["ID_ESCOLA", "NO_ESCOLA", "SG_UF", "NO_MUNICIPIO", "REDE"]
        missing = [c for c in req_cols if c not in df_sheet.columns]
        if missing:
            raise ValueError(f"Colunas obrigatórias ausentes na aba {sheet_name}: {missing}")

        # Garantir strings para colunas do tipo object
        for c in df_sheet.columns:
            if df_sheet[c].dtype == object:
                df_sheet[c] = df_sheet[c].astype(str)

        out_path = raw_ideb_dir / out_name
        df_sheet.to_parquet(out_path, index=False)
        print(f"  Salvo em: {out_path} ({len(df_sheet)} linhas)")

    print("\n=== Importação do IDEB Concluída com Sucesso! ===")

if __name__ == "__main__":
    run()
