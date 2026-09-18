#!/usr/bin/env python3
"""
transformar_ideb_painel.py

Script para transformação dos dados oficiais do IDEB (INEP/MEC) do formato wide
para o formato analítico padronizado tidy/long:
(ID_ESCOLA x ANO_IDEB x ETAPA).

Extrai e padroniza:
- IDEB Observado (escala 0 a 10);
- Metas Projetadas do IDEB (quando disponíveis no ciclo 2007-2021);
- Componente de Aprendizado Padronizado N (0 a 10);
- Componente de Fluxo Escolar P (média harmônica das taxas de aprovação);
- Taxa de Aprovação Total utilizada no IDEB;
- Categorização de status (DIVULGADO, NAO_DIVULGADO_CRITERIO_INEP, SEM_PARTICIPACAO).

Fontes:
- data/raw/ideb/ideb_anos_iniciais_raw.parquet
- data/raw/ideb/ideb_anos_finais_raw.parquet
- data/raw/ideb/ideb_ensino_medio_raw.parquet

Saídas:
- data/processed/ideb/ideb_escolas_parana_tidy.parquet
- data/processed/ideb/ideb_escolas_parana_tidy.csv
"""

import re
from pathlib import Path
import pandas as pd
import numpy as np

def clean_numeric(val):
    """Converte valor numérico string com vírgula para float."""
    if pd.isna(val):
        return np.nan
    s = str(val).strip()
    if s in ["-", "ND", "null", "nan", "", "None"]:
        return np.nan
    s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return np.nan

def classificar_status_ideb(val_str):
    """Classifica o status de divulgação do IDEB pelo INEP."""
    if pd.isna(val_str):
        return "DADO_AUSENTE"
    s = str(val_str).strip()
    if s == "ND":
        return "NAO_DIVULGADO_CRITERIO_INEP"
    elif s in ["-", ""]:
        return "SEM_PARTICIPACAO"
    else:
        num = clean_numeric(s)
        if pd.notna(num):
            return "DIVULGADO"
        return "DADO_AUSENTE"

def run():
    print("=== Iniciando Transformação dos Dados do IDEB (Wide para Tidy) ===")
    base_dir = Path(__file__).resolve().parent.parent.parent
    raw_dir = base_dir / "data" / "raw" / "ideb"
    proc_dir = base_dir / "data" / "processed" / "ideb"
    proc_dir.mkdir(parents=True, exist_ok=True)

    etapas = [
        ("ideb_anos_iniciais_raw.parquet", "Anos Iniciais (1º-5º)"),
        ("ideb_anos_finais_raw.parquet", "Anos Finais (6º-9º)"),
        ("ideb_ensino_medio_raw.parquet", "Ensino Médio"),
    ]

    dfs_tidy = []

    for file_name, etapa_label in etapas:
        file_path = raw_dir / file_name
        if not file_path.exists():
            print(f"AVISO: Arquivo {file_path} não encontrado!")
            continue

        print(f"\nProcessando etapa: {etapa_label} ({file_name})...")
        df_raw = pd.read_parquet(file_path)
        cols = df_raw.columns.tolist()

        # Identificar anos pelas colunas VL_OBSERVADO_{ano}
        anos = sorted(list(set([
            int(m.group(1)) for c in cols
            if (m := re.search(r'VL_OBSERVADO_(\d{4})', c))
        ])))
        print(f"  Anos de IDEB identificados: {anos}")

        for ano in anos:
            col_obs = f"VL_OBSERVADO_{ano}"
            col_proj = f"VL_PROJECAO_{ano}"
            col_n = f"VL_NOTA_MEDIA_{ano}"
            col_p = f"VL_INDICADOR_REND_{ano}"
            col_aprov = f"VL_APROVACAO_{ano}_SI_4"

            s_obs = df_raw[col_obs] if col_obs in cols else pd.Series(np.nan, index=df_raw.index)
            s_proj = df_raw[col_proj] if col_proj in cols else pd.Series(np.nan, index=df_raw.index)
            s_n = df_raw[col_n] if col_n in cols else pd.Series(np.nan, index=df_raw.index)
            s_p = df_raw[col_p] if col_p in cols else pd.Series(np.nan, index=df_raw.index)
            s_aprov = df_raw[col_aprov] if col_aprov in cols else pd.Series(np.nan, index=df_raw.index)

            status_ideb = s_obs.apply(classificar_status_ideb)

            sub_df = pd.DataFrame({
                "SG_UF": df_raw["SG_UF"].astype(str),
                "CO_MUNICIPIO": df_raw["CO_MUNICIPIO"].astype(str).str.replace(r'\.0$', '', regex=True),
                "NO_MUNICIPIO": df_raw["NO_MUNICIPIO"].astype(str),
                "ID_ESCOLA": pd.to_numeric(df_raw["ID_ESCOLA"], errors="coerce").astype("Int64"),
                "NO_ESCOLA": df_raw["NO_ESCOLA"].astype(str),
                "REDE": df_raw["REDE"].astype(str),
                "ETAPA": etapa_label,
                "ANO_IDEB": int(ano),
                "IDEB_OBSERVADO": s_obs.apply(clean_numeric),
                "IDEB_META": s_proj.apply(clean_numeric),
                "IDEB_COMPONENTE_N": s_n.apply(clean_numeric),
                "IDEB_COMPONENTE_P": s_p.apply(clean_numeric),
                "TAXA_APROVACAO_IDEB": s_aprov.apply(clean_numeric),
                "STATUS_IDEB": status_ideb,
                "FONTE_IDEB": "INEP/MEC - Divulgação dos Resultados do Ideb por Escola (Paraná)"
            })

            dfs_tidy.append(sub_df)

    df_tidy_all = pd.concat(dfs_tidy, ignore_index=True)
    df_tidy_all = df_tidy_all[df_tidy_all["ID_ESCOLA"].notna()].copy()
    df_tidy_all["ID_ESCOLA"] = df_tidy_all["ID_ESCOLA"].astype(int)
    df_tidy_all = df_tidy_all.sort_values(by=["ID_ESCOLA", "ETAPA", "ANO_IDEB"]).reset_index(drop=True)

    out_parquet = proc_dir / "ideb_escolas_parana_tidy.parquet"
    out_csv = proc_dir / "ideb_escolas_parana_tidy.csv"

    df_tidy_all.to_parquet(out_parquet, index=False)
    df_tidy_all.to_csv(out_csv, sep=";", index=False, encoding="utf-8")

    print(f"\nBase IDEB Tidy gerada com sucesso!")
    print(f"  Parquet: {out_parquet} ({len(df_tidy_all)} registros)")
    print(f"  CSV: {out_csv}")
    print("\nEstatísticas de Cobertura do IDEB Observado por Ano:")
    stats = df_tidy_all.groupby(["ANO_IDEB", "ETAPA"])["IDEB_OBSERVADO"].agg(
        total_com_ideb=lambda x: x.notna().sum(),
        media_ideb="mean"
    )
    print(stats.to_string())

if __name__ == "__main__":
    run()
