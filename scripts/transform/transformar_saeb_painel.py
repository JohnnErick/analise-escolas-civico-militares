#!/usr/bin/env python3
"""
transformar_saeb_painel.py

Script para transformação dos dados brutos do SAEB/IDEB do formato wide (colunas por ano)
para o formato analítico tidy/long (uma linha por escola x etapa x ano).
Aplica tratamento correto de pontuação decimal (evitando perda de dados de 2015),
categoriza os motivos de ausência de resultado e padroniza as variáveis oficiais do INEP.

Fontes:
- data/raw/saeb/saeb_anos_iniciais_raw.parquet
- data/raw/saeb/saeb_anos_finais_raw.parquet
- data/raw/saeb/saeb_ensino_medio_raw.parquet

Saídas:
- data/processed/saeb/saeb_escolas_parana_tidy.parquet
- data/processed/saeb/saeb_escolas_parana_tidy.csv
"""

import re
from pathlib import Path
import pandas as pd
import numpy as np

def clean_numeric(val):
    """Converte valores string com vírgula ou formato misto para float numérico."""
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

def classificar_status_participacao(val_str):
    """Classifica o status de participação e divulgação oficial do INEP."""
    if pd.isna(val_str):
        return "DADO_AUSENTE"
    s = str(val_str).strip()
    if s == "ND":
        return "NAO_DIVULGADO_CRITERIO_INEP"
    elif s in ["-", ""]:
        return "SEM_PARTICIPACAO"
    else:
        # Se for conversível para número, é DIVULGADO
        clean_num = clean_numeric(s)
        if pd.notna(clean_num):
            return "DIVULGADO"
        return "DADO_AUSENTE"

def run():
    print("=== Iniciando Transformação dos Dados SAEB/INEP (Wide para Tidy) ===")
    base_dir = Path(__file__).resolve().parent.parent.parent
    raw_dir = base_dir / "data" / "raw" / "saeb"
    proc_dir = base_dir / "data" / "processed" / "saeb"
    proc_dir.mkdir(parents=True, exist_ok=True)

    etapas = [
        ("saeb_anos_iniciais_raw.parquet", "Anos Iniciais (1º-5º)"),
        ("saeb_anos_finais_raw.parquet", "Anos Finais (6º-9º)"),
        ("saeb_ensino_medio_raw.parquet", "Ensino Médio")
    ]

    dfs_tidy = []

    for file_name, etapa_label in etapas:
        file_path = raw_dir / file_name
        if not file_path.exists():
            print(f"AVISO: Arquivo {file_path} não encontrado!")
            continue

        print(f"\nProcessando etapa: {etapa_label} ({file_name})...")
        df_raw = pd.read_parquet(file_path)

        # Identificar anos disponíveis pelas colunas
        cols = df_raw.columns.tolist()
        anos = sorted(list(set([
            int(m.group(0)) for c in cols
            if (m := re.search(r'20\d{2}', c))
        ])))
        print(f"  Anos identificados nas colunas: {anos}")

        for ano in anos:
            col_mat = f"VL_NOTA_MATEMATICA_{ano}"
            col_port = f"VL_NOTA_PORTUGUES_{ano}"
            col_media = f"VL_NOTA_MEDIA_{ano}"
            col_ideb = f"VL_OBSERVADO_{ano}"
            col_rend = f"VL_INDICADOR_REND_{ano}"
            col_aprov = f"VL_APROVACAO_{ano}_SI_4"

            # Séries brutas
            s_mat = df_raw[col_mat] if col_mat in cols else pd.Series(np.nan, index=df_raw.index)
            s_port = df_raw[col_port] if col_port in cols else pd.Series(np.nan, index=df_raw.index)
            s_media = df_raw[col_media] if col_media in cols else pd.Series(np.nan, index=df_raw.index)
            s_ideb = df_raw[col_ideb] if col_ideb in cols else pd.Series(np.nan, index=df_raw.index)
            s_rend = df_raw[col_rend] if col_rend in cols else pd.Series(np.nan, index=df_raw.index)
            s_aprov = df_raw[col_aprov] if col_aprov in cols else pd.Series(np.nan, index=df_raw.index)

            # Classificação do status com base no registro de Matemática / Português
            status_part = s_mat.apply(classificar_status_participacao)

            # Conversão limpa para numérico
            num_mat = s_mat.apply(clean_numeric)
            num_port = s_port.apply(clean_numeric)
            num_media = s_media.apply(clean_numeric)
            num_ideb = s_ideb.apply(clean_numeric)
            num_rend = s_rend.apply(clean_numeric)
            num_aprov = s_aprov.apply(clean_numeric)

            sub_df = pd.DataFrame({
                "SG_UF": df_raw["SG_UF"].astype(str),
                "CO_MUNICIPIO": df_raw["CO_MUNICIPIO"].astype(str).str.replace(r'\.0$', '', regex=True),
                "NO_MUNICIPIO": df_raw["NO_MUNICIPIO"].astype(str),
                "ID_ESCOLA": pd.to_numeric(df_raw["ID_ESCOLA"], errors="coerce").astype("Int64"),
                "NO_ESCOLA": df_raw["NO_ESCOLA"].astype(str),
                "REDE": df_raw["REDE"].astype(str),
                "ETAPA": etapa_label,
                "ANO_SAEB": int(ano),
                "SAEB_MATEMATICA": num_mat,
                "SAEB_PORTUGUES": num_port,
                "SAEB_NOTA_MEDIA": num_media,
                "IDEB_OBSERVADO": num_ideb,
                "INDICADOR_RENDIMENTO": num_rend,
                "TAXA_APROVACAO": num_aprov,
                "STATUS_PARTICIPACAO_SAEB": status_part,
                "FONTE_SAEB": "INEP/MEC - Divulgação dos Resultados do Ideb e Saeb por Escola (Paraná)"
            })
            dfs_tidy.append(sub_df)

    df_tidy_all = pd.concat(dfs_tidy, ignore_index=True)
    # Filtro de ID_ESCOLA válido
    df_tidy_all = df_tidy_all[df_tidy_all["ID_ESCOLA"].notna()].copy()
    df_tidy_all["ID_ESCOLA"] = df_tidy_all["ID_ESCOLA"].astype(int)

    # Ordenar logicamente
    df_tidy_all = df_tidy_all.sort_values(by=["ID_ESCOLA", "ETAPA", "ANO_SAEB"]).reset_index(drop=True)

    out_parquet = proc_dir / "saeb_escolas_parana_tidy.parquet"
    out_csv = proc_dir / "saeb_escolas_parana_tidy.csv"

    df_tidy_all.to_parquet(out_parquet, index=False)
    df_tidy_all.to_csv(out_csv, sep=";", index=False, encoding="utf-8")

    print(f"\nBase SAEB Tidy gerada com sucesso!")
    print(f"  Parquet: {out_parquet} ({len(df_tidy_all)} registros)")
    print(f"  CSV: {out_csv}")
    print("\nEstatísticas de Proficiência em Matemática por Ano:")
    stats_mat = df_tidy_all.groupby("ANO_SAEB")["SAEB_MATEMATICA"].agg(
        total_avaliadas=lambda x: x.notna().sum(),
        media_geral="mean"
    )
    print(stats_mat.to_string())

if __name__ == "__main__":
    run()
