#!/usr/bin/env python3
"""
integrar_ccm_saeb.py

Script para integração metodológica dos dados oficiais do SAEB/IDEB (INEP/MEC)
com a base histórica anualizada das escolas cívico-militares do Paraná.

Chave primária de matching: ID_ESCOLA (INEP) e ANO / ANO_SAEB.

Fontes:
- data/processed/historico_ccm_por_ano.csv
- data/processed/historico_ccm_matching_inep.csv
- data/processed/saeb/saeb_escolas_parana_tidy.parquet

Saídas:
- data/processed/saeb/ccm_saeb_matriz_integrada.csv
- data/processed/saeb/ccm_saeb_matriz_integrada.parquet
- data/processed/saeb/ccm_saeb_serie_historica_completa.csv
- data/processed/saeb/ccm_saeb_serie_historica_completa.parquet
- data/processed/saeb/auditoria_matching_ccm_saeb.csv
"""

from pathlib import Path
import pandas as pd
import numpy as np

def run():
    print("=== Iniciando Integração Metodológica CCM x SAEB ===")
    base_dir = Path(__file__).resolve().parent.parent.parent
    proc_dir = base_dir / "data" / "processed" / "saeb"
    proc_dir.mkdir(parents=True, exist_ok=True)

    # 1. Carregar base histórica CCM anualizada congelada
    path_ccm_ano = base_dir / "data" / "processed" / "historico_ccm_por_ano.csv"
    path_matching = base_dir / "data" / "processed" / "historico_ccm_matching_inep.csv"
    path_saeb_tidy = proc_dir / "saeb_escolas_parana_tidy.parquet"

    df_ccm = pd.read_csv(path_ccm_ano, sep=";")
    df_mt = pd.read_csv(path_matching, sep=";")
    df_saeb = pd.read_parquet(path_saeb_tidy)

    print(f"Base CCM anualizada: {len(df_ccm)} registros ({df_ccm['codigo_inep'].nunique()} escolas x {df_ccm['ano'].nunique()} anos)")
    print(f"Base de matching INEP: {len(df_mt)} escolas")
    print(f"Base SAEB Tidy Paraná: {len(df_saeb)} registros totais")

    ccm_ineps = sorted(df_mt["codigo_inep"].unique().tolist())

    # 2. Auditoria de Matching Cadastral Escolar (Escolas CCM no Cadastro SAEB)
    # Verificar a presença de cada código INEP da base CCM na base do SAEB
    saeb_escolas_unicas = df_saeb.drop_duplicates(subset=["ID_ESCOLA"]).set_index("ID_ESCOLA")
    auditoria_rows = []

    anos_saeb_disponiveis = sorted(df_saeb["ANO_SAEB"].unique().tolist())

    for _, r_mt in df_mt.iterrows():
        cod = int(r_mt["codigo_inep"])
        nome_mt = r_mt["nome_escola_cadastro"]
        mun_mt = r_mt["municipio_cadastro"]
        st_mt = r_mt["status_matching"]

        if cod == 41146093:
            st_match = "AMBIGUO"
            obs = "Erro material do Edital 125/2025 isolado; no SAEB corresponde à escola homônima de São José dos Pinhais."
        elif cod in saeb_escolas_unicas.index:
            st_match = "CONFIRMADO"
            obs = "Código INEP localizado com sucesso na base oficial de divulgação do SAEB/IDEB do INEP."
        else:
            st_match = "NAO_ENCONTRADO"
            obs = "Código INEP não localizado na base do SAEB."

        for ano_s in anos_saeb_disponiveis:
            auditoria_rows.append({
                "ano_saeb": ano_s,
                "codigo_inep": cod,
                "nome_escola": nome_mt,
                "municipio": mun_mt,
                "status_matching": st_match,
                "fonte_saeb": "INEP/MEC - Divulgação dos Resultados do Ideb e Saeb por Escola (Paraná)",
                "observacao": obs
            })

    df_auditoria = pd.DataFrame(auditoria_rows)
    path_auditoria_csv = proc_dir / "auditoria_matching_ccm_saeb.csv"
    df_auditoria.to_csv(path_auditoria_csv, sep=";", index=False, encoding="utf-8")
    print(f"Auditoria de matching cadastral salva em: {path_auditoria_csv} ({len(df_auditoria)} registros)")

    # 3. Construção da Matriz Integrada CCM x SAEB no período do projeto (2020 a 2026)
    # Cruzamento de df_ccm com df_saeb
    # Nota: Anos ímpares com edição do SAEB: 2021 e 2023. Anos pares (2020, 2022, 2024, 2026) e 2025 não possuem edição final do SAEB.
    # Etapas de ensino presentes nas escolas: Anos Finais (6º-9º) e Ensino Médio
    # Cada escola pode ofertar uma ou ambas as etapas. Realizamos a integração por etapa.

    sub_saeb_ccm = df_saeb[df_saeb["ID_ESCOLA"].isin(ccm_ineps)].copy()
    etapas_escolas = sub_saeb_ccm[["ID_ESCOLA", "ETAPA"]].drop_duplicates()

    # Expandir df_ccm por cada etapa ofertada pela escola
    df_ccm_expandido = pd.merge(
        df_ccm,
        etapas_escolas,
        left_on="codigo_inep",
        right_on="ID_ESCOLA",
        how="inner"
    ).drop(columns=["ID_ESCOLA"])

    print(f"Base CCM expandida por etapas ofertadas: {len(df_ccm_expandido)} registros")

    # Realizar merge com dados do SAEB por (codigo_inep == ID_ESCOLA), (ano == ANO_SAEB) e (ETAPA == ETAPA)
    df_integrada = pd.merge(
        df_ccm_expandido,
        sub_saeb_ccm[[
            "ID_ESCOLA", "ETAPA", "ANO_SAEB",
            "SAEB_MATEMATICA", "SAEB_PORTUGUES", "SAEB_NOTA_MEDIA",
            "IDEB_OBSERVADO", "INDICADOR_RENDIMENTO", "TAXA_APROVACAO",
            "STATUS_PARTICIPACAO_SAEB"
        ]],
        left_on=["codigo_inep", "ETAPA", "ano"],
        right_on=["ID_ESCOLA", "ETAPA", "ANO_SAEB"],
        how="left"
    ).drop(columns=["ID_ESCOLA", "ANO_SAEB"])

    # Tratamento consistente para anos sem edição do SAEB
    anos_com_saeb = [2021, 2023]
    for idx, row in df_integrada.iterrows():
        ano = row["ano"]
        if ano not in anos_com_saeb:
            df_integrada.at[idx, "STATUS_PARTICIPACAO_SAEB"] = "SEM_EDICAO_SAEB_ANO_PAR_OU_INTERMEDIARIO"

    # Salvar matriz integrada do período
    path_matriz_integ_csv = proc_dir / "ccm_saeb_matriz_integrada.csv"
    path_matriz_integ_parquet = proc_dir / "ccm_saeb_matriz_integrada.parquet"

    df_integrada.to_csv(path_matriz_integ_csv, sep=";", index=False, encoding="utf-8")
    df_integrada.to_parquet(path_matriz_integ_parquet, index=False)

    print(f"Matriz Integrada CCM x SAEB salva em:")
    print(f"  CSV: {path_matriz_integ_csv} ({len(df_integrada)} linhas)")
    print(f"  Parquet: {path_matriz_integ_parquet}")

    # 4. Construção da Série Histórica Longitudinal Completa (2005 a 2025)
    # Para subsidiar a análise histórica pré-programa (2005 a 2019)
    df_serie_completa = pd.merge(
        sub_saeb_ccm,
        df_mt[["codigo_inep", "status_matching", "nivel_confianca"]],
        left_on="ID_ESCOLA",
        right_on="codigo_inep",
        how="left"
    ).drop(columns=["codigo_inep"])

    # Associar ano_inicio_ccm da matriz histórica
    inicio_map = df_ccm.drop_duplicates("codigo_inep").set_index("codigo_inep")["ano_inicio_ccm"].to_dict()
    df_serie_completa["ano_inicio_ccm"] = df_serie_completa["ID_ESCOLA"].map(inicio_map)

    path_serie_csv = proc_dir / "ccm_saeb_serie_historica_completa.csv"
    path_serie_parquet = proc_dir / "ccm_saeb_serie_historica_completa.parquet"

    df_serie_completa.to_csv(path_serie_csv, sep=";", index=False, encoding="utf-8")
    df_serie_completa.to_parquet(path_serie_parquet, index=False)

    print(f"\nSérie Histórica Longitudinal Completa salva em:")
    print(f"  CSV: {path_serie_csv} ({len(df_serie_completa)} linhas)")
    print(f"  Parquet: {path_serie_parquet}")
    print("\n=== Integração Concluída com Sucesso! ===")

if __name__ == "__main__":
    run()
