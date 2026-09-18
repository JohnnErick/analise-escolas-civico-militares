#!/usr/bin/env python3
"""
transformar_rendimento_painel.py

Script para transformação dos dados de Taxas de Rendimento Escolar (INEP/MEC)
do formato wide (colunas por etapa) para o formato tidy/long:
(ID_ESCOLA x ANO x ETAPA).

Converte e padroniza separadores decimais, categoriza rigorosamente os motivos
de ausência de informação e valida os intervalos percentuais (0 a 100%).

Fontes:
- data/raw/rendimento/rendimento_parana_raw.parquet

Saídas:
- data/processed/rendimento/rendimento_escolas_parana_tidy.parquet
- data/processed/rendimento/rendimento_escolas_parana_tidy.csv
"""

from pathlib import Path
import pandas as pd
import numpy as np

def clean_rate(val):
    """Converte valor percentual string com vírgula ou formato misto para float numérico."""
    if pd.isna(val):
        return np.nan
    s = str(val).strip()
    if s in ["--", "-", "ND", "null", "nan", "", "None"]:
        return np.nan
    s = s.replace(",", ".")
    try:
        f = float(s)
        # Se válido entre 0 e 100
        if 0.0 <= f <= 100.0:
            return f
        return np.nan
    except ValueError:
        return np.nan

def classificar_status_rendimento(val_str):
    """Classifica o status de divulgação da taxa de rendimento escolar."""
    if pd.isna(val_str):
        return "DADO_AUSENTE"
    s = str(val_str).strip()
    if s in ["--", "-"]:
        return "SEM_INFORMACAO_OU_NAO_OFERTADO"
    elif s == "ND":
        return "NAO_DIVULGADO_CRITERIO_INEP"
    else:
        num = clean_rate(s)
        if pd.notna(num):
            return "DIVULGADO"
        return "DADO_AUSENTE"

def run():
    print("=== Iniciando Transformação das Taxas de Rendimento (Wide para Tidy) ===")
    base_dir = Path(__file__).resolve().parent.parent.parent
    raw_path = base_dir / "data" / "raw" / "rendimento" / "rendimento_parana_raw.parquet"
    proc_dir = base_dir / "data" / "processed" / "rendimento"
    proc_dir.mkdir(parents=True, exist_ok=True)

    if not raw_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {raw_path}")

    print(f"Lendo base bruta de rendimento: {raw_path}")
    df_raw = pd.read_parquet(raw_path)
    print(f"Registros brutos: {len(df_raw)}")

    etapas = [
        ("Anos Iniciais (1º-5º)", "APROV_ANOS_INICIAIS", "REPROV_ANOS_INICIAIS", "ABAND_ANOS_INICIAIS"),
        ("Anos Finais (6º-9º)", "APROV_ANOS_FINAIS", "REPROV_ANOS_FINAIS", "ABAND_ANOS_FINAIS"),
        ("Ensino Médio", "APROV_ENSINO_MEDIO", "REPROV_ENSINO_MEDIO", "ABAND_ENSINO_MEDIO"),
    ]

    dfs_tidy = []

    for etapa_label, col_aprov, col_reprov, col_aband in etapas:
        print(f"Processando etapa: {etapa_label}...")

        s_aprov_raw = df_raw[col_aprov]
        s_reprov_raw = df_raw[col_reprov]
        s_aband_raw = df_raw[col_aband]

        num_aprov = s_aprov_raw.apply(clean_rate)
        num_reprov = s_reprov_raw.apply(clean_rate)
        num_aband = s_aband_raw.apply(clean_rate)

        status_rend = s_aprov_raw.apply(classificar_status_rendimento)

        sub_df = pd.DataFrame({
            "SG_UF": "PR",
            "CO_MUNICIPIO": df_raw["CO_MUNICIPIO"],
            "NO_MUNICIPIO": df_raw["NO_MUNICIPIO"],
            "ID_ESCOLA": df_raw["CO_ENTIDADE"],
            "NO_ESCOLA": df_raw["NO_ENTIDADE"],
            "REDE": df_raw["NO_DEPENDENCIA"],
            "ANO": df_raw["ANO"],
            "ETAPA": etapa_label,
            "TAXA_APROVACAO": num_aprov,
            "TAXA_REPROVACAO": num_reprov,
            "TAXA_ABANDONO": num_aband,
            "STATUS_RENDIMENTO": status_rend,
            "FONTE_RENDIMENTO": "INEP/MEC - Censo Escolar da Educação Básica (Taxas de Rendimento)"
        })

        dfs_tidy.append(sub_df)

    df_tidy_all = pd.concat(dfs_tidy, ignore_index=True)
    df_tidy_all = df_tidy_all.sort_values(by=["ID_ESCOLA", "ETAPA", "ANO"]).reset_index(drop=True)

    out_parquet = proc_dir / "rendimento_escolas_parana_tidy.parquet"
    out_csv = proc_dir / "rendimento_escolas_parana_tidy.csv"

    df_tidy_all.to_parquet(out_parquet, index=False)
    df_tidy_all.to_csv(out_csv, sep=";", index=False, encoding="utf-8")

    print(f"\nBase Rendimento Tidy gerada com sucesso!")
    print(f"  Parquet: {out_parquet} ({len(df_tidy_all)} registros)")
    print(f"  CSV: {out_csv}")
    print("\nEstatísticas de Cobertura por Ano (com taxa de aprovação válida):")
    stats = df_tidy_all.groupby(["ANO", "ETAPA"])["TAXA_APROVACAO"].agg(
        total_com_taxa=lambda x: x.notna().sum(),
        media_aprovacao="mean"
    )
    print(stats.to_string())

if __name__ == "__main__":
    run()
