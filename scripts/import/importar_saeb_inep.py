#!/usr/bin/env python3
"""
importar_saeb_inep.py

Script para leitura, validação estrutural e importação dos dados brutos
do SAEB/IDEB disponibilizados oficialmente pelo INEP/MEC para o Estado do Paraná.

Fonte:
- data/raw/saeb/divulgacao_pr_consolidado.xlsx

Saídas:
- data/raw/saeb/saeb_anos_iniciais_raw.parquet
- data/raw/saeb/saeb_anos_finais_raw.parquet
- data/raw/saeb/saeb_ensino_medio_raw.parquet
"""

import os
from pathlib import Path
import pandas as pd

def run():
    print("=== Iniciando Importação dos Dados Brutos do SAEB/INEP ===")
    base_dir = Path(__file__).resolve().parent.parent.parent
    raw_dir = base_dir / "data" / "raw" / "saeb"
    input_file = raw_dir / "divulgacao_pr_consolidado.xlsx"

    if not input_file.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {input_file}")

    print(f"Lendo arquivo bruto consolidado: {input_file}")
    xl = pd.ExcelFile(input_file)
    sheet_names = xl.sheet_names
    print(f"Abas encontradas ({len(sheet_names)}): {sheet_names}")

    expected_sheets = {
        "divulgacao_anos_iniciais": "saeb_anos_iniciais_raw.parquet",
        "divulgacao_anos_finais": "saeb_anos_finais_raw.parquet",
        "divulgacao_ensino_medio": "saeb_ensino_medio_raw.parquet"
    }

    for sheet, out_name in expected_sheets.items():
        if sheet not in sheet_names:
            print(f"AVISO: Aba '{sheet}' não encontrada no arquivo!")
            continue

        print(f"\nImportando aba: {sheet} ...")
        df_sheet = pd.read_excel(xl, sheet_name=sheet)
        print(f"  Registros importados: {len(df_sheet)}")
        print(f"  Colunas ({len(df_sheet.columns)}): {df_sheet.columns.tolist()[:8]}...")

        # Validação de colunas fundamentais
        req_cols = ["ID_ESCOLA", "NO_ESCOLA", "SG_UF", "NO_MUNICIPIO", "REDE"]
        missing_req = [c for c in req_cols if c not in df_sheet.columns]
        if missing_req:
            raise ValueError(f"Aba '{sheet}' não contém colunas essenciais: {missing_req}")

        # Garantir compatibilidade de tipos mistos no parquet bruto (converter colunas object para str)
        for c in df_sheet.columns:
            if df_sheet[c].dtype == object:
                df_sheet[c] = df_sheet[c].astype(str)

        # Salvar em parquet bruto
        out_path = raw_dir / out_name
        df_sheet.to_parquet(out_path, index=False)
        print(f"  Salvo em: {out_path} ({len(df_sheet)} linhas)")

    print("\n=== Importação de Dados Brutos Concluída com Sucesso! ===")

if __name__ == "__main__":
    run()
