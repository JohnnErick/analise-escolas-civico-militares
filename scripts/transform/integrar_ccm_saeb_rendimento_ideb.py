#!/usr/bin/env python3
"""
integrar_ccm_saeb_rendimento_ideb.py

Script para integração metodológica dos indicadores oficiais de:
1. Histórico Temporal dos Colégios Cívico-Militares (CCM) do Paraná (2020 a 2026);
2. Resultados Oficiais do SAEB (Língua Portuguesa, Matemática, Média Padronizada N);
3. Taxas Oficiais de Rendimento Escolar (Aprovação, Reprovação e Abandono);
4. Resultados e Metas do IDEB (IDEB Observado, Componentes N e P, Metas Projetadas).

Chave Primária de Ligação: codigo_inep (ID_ESCOLA), ano e ETAPA.

Preserva integralmente o status institucional cívico-militar congelado
em data/processed/historico_ccm_por_ano.csv sem recalcular ou imputar valores.

Fontes:
- data/processed/saeb/ccm_saeb_matriz_integrada.parquet
- data/processed/rendimento/rendimento_escolas_parana_tidy.parquet
- data/processed/ideb/ideb_escolas_parana_tidy.parquet
- data/processed/historico_ccm_matching_inep.csv

Saídas:
- data/processed/ccm_saeb_rendimento_ideb.parquet
- data/processed/ccm_saeb_rendimento_ideb.csv
- data/processed/ccm_saeb_rendimento_ideb_serie_completa.parquet
- data/processed/ccm_saeb_rendimento_ideb_serie_completa.csv
- data/processed/auditoria_matching_rendimento_ideb.csv
"""

from pathlib import Path
import pandas as pd
import numpy as np

def run():
    print("=== Iniciando Integração Completa: CCM x SAEB x Rendimento x IDEB ===")
    base_dir = Path(__file__).resolve().parent.parent.parent
    proc_dir = base_dir / "data" / "processed"

    # 1. Carregar bases de entrada
    path_ccm_saeb = proc_dir / "saeb" / "ccm_saeb_matriz_integrada.parquet"
    path_rend = proc_dir / "rendimento" / "rendimento_escolas_parana_tidy.parquet"
    path_ideb = proc_dir / "ideb" / "ideb_escolas_parana_tidy.parquet"
    path_mt = proc_dir / "historico_ccm_matching_inep.csv"
    path_ccm_ano = proc_dir / "historico_ccm_por_ano.csv"

    # Fallback para CSV se parquet falhar
    df_ccm_saeb = pd.read_parquet(path_ccm_saeb) if path_ccm_saeb.exists() else pd.read_csv(proc_dir / "saeb" / "ccm_saeb_matriz_integrada.csv", sep=";")
    df_rend = pd.read_parquet(path_rend) if path_rend.exists() else pd.read_csv(proc_dir / "rendimento" / "rendimento_escolas_parana_tidy.csv", sep=";")
    df_ideb = pd.read_parquet(path_ideb) if path_ideb.exists() else pd.read_csv(proc_dir / "ideb" / "ideb_escolas_parana_tidy.csv", sep=";")
    df_mt = pd.read_csv(path_mt, sep=";")
    df_ccm_ano = pd.read_csv(path_ccm_ano, sep=";")

    print(f"Base CCM x SAEB Matriz: {len(df_ccm_saeb)} registros")
    print(f"Base Rendimento Tidy: {len(df_rend)} registros")
    print(f"Base IDEB Tidy: {len(df_ideb)} registros")
    print(f"Escolas CCM no matching cadastral: {len(df_mt)}")

    ccm_ineps = sorted(df_mt["codigo_inep"].unique().tolist())

    # 2. Auditoria Cadastral de Correspondência (Rendimento e IDEB)
    rend_ineps = set(df_rend["ID_ESCOLA"].unique())
    ideb_ineps = set(df_ideb["ID_ESCOLA"].unique())

    auditoria_rows = []
    for _, r in df_mt.iterrows():
        cod = int(r["codigo_inep"])
        nome = r["nome_escola_cadastro"]
        mun = r["municipio_cadastro"]

        # Status Rendimento
        if cod in rend_ineps:
            st_rend = "CONFIRMADO"
            obs_rend = "Código INEP localizado nas tabelas de taxas de rendimento do Censo Escolar."
        elif cod == 41167090:
            st_rend = "FORA_DA_POPULACAO_HISTORICA"
            obs_rend = "Escola de criação recente (Edital 125/2025); sem turmas no período do Censo 2017-2023."
        else:
            st_rend = "NAO_ENCONTRADO"
            obs_rend = "Código INEP não localizado na base de rendimento."

        # Status IDEB
        if cod in ideb_ineps:
            st_ideb = "CONFIRMADO"
            obs_ideb = "Código INEP localizado na base oficial de divulgação do IDEB."
        else:
            st_ideb = "NAO_ENCONTRADO"
            obs_ideb = "Código INEP não localizado na base do IDEB."

        auditoria_rows.append({
            "codigo_inep": cod,
            "nome_escola": nome,
            "municipio": mun,
            "status_matching_ccm": r["status_matching"],
            "status_matching_rendimento": st_rend,
            "obs_rendimento": obs_rend,
            "status_matching_ideb": st_ideb,
            "obs_ideb": obs_ideb
        })

    df_auditoria = pd.DataFrame(auditoria_rows)
    path_auditoria_csv = proc_dir / "auditoria_matching_rendimento_ideb.csv"
    df_auditoria.to_csv(path_auditoria_csv, sep=";", index=False, encoding="utf-8")
    print(f"Auditoria de matching cadastral salva em: {path_auditoria_csv}")

    # 3. Integração com a Matriz do Período Institucional (2020 a 2026)
    # Selecionar colunas de Rendimento
    cols_rend = [
        "ID_ESCOLA", "ANO", "ETAPA",
        "TAXA_APROVACAO", "TAXA_REPROVACAO", "TAXA_ABANDONO", "STATUS_RENDIMENTO"
    ]
    sub_rend = df_rend[df_rend["ID_ESCOLA"].isin(ccm_ineps)][cols_rend].copy()

    # Selecionar colunas de IDEB
    cols_ideb = [
        "ID_ESCOLA", "ANO_IDEB", "ETAPA",
        "IDEB_OBSERVADO", "IDEB_META", "IDEB_COMPONENTE_N", "IDEB_COMPONENTE_P",
        "TAXA_APROVACAO_IDEB", "STATUS_IDEB"
    ]
    sub_ideb = df_ideb[df_ideb["ID_ESCOLA"].isin(ccm_ineps)][cols_ideb].copy()

    # Remover colunas preliminares para que venham das bases completas de rendimento e ideb
    df_base_ccm = df_ccm_saeb.drop(columns=[
        c for c in ["TAXA_APROVACAO", "IDEB_OBSERVADO", "INDICADOR_RENDIMENTO"]
        if c in df_ccm_saeb.columns
    ])

    # Merge Rendimento com Matriz CCM x SAEB
    df_integ = pd.merge(
        df_base_ccm,
        sub_rend,
        left_on=["codigo_inep", "ano", "ETAPA"],
        right_on=["ID_ESCOLA", "ANO", "ETAPA"],
        how="left"
    ).drop(columns=["ID_ESCOLA", "ANO"])

    # Merge IDEB com Matriz CCM x SAEB
    df_integ = pd.merge(
        df_integ,
        sub_ideb,
        left_on=["codigo_inep", "ano", "ETAPA"],
        right_on=["ID_ESCOLA", "ANO_IDEB", "ETAPA"],
        how="left"
    ).drop(columns=["ID_ESCOLA", "ANO_IDEB"])

    # Tratamento consistente dos status para anos sem coleta/divulgação
    anos_com_rendimento = [2020, 2021, 2022, 2023]
    anos_com_ideb = [2021, 2023]

    for idx, row in df_integ.iterrows():
        ano = row["ano"]
        cod = row["codigo_inep"]

        # Ajuste status rendimento
        if pd.isna(row["STATUS_RENDIMENTO"]):
            if cod == 41167090:
                df_integ.at[idx, "STATUS_RENDIMENTO"] = "FORA_DA_POPULACAO_HISTORICA"
            elif ano not in anos_com_rendimento:
                df_integ.at[idx, "STATUS_RENDIMENTO"] = "SEM_INFORMACAO_ANO_FUTURO_OU_NAO_PUBLICADO"
            else:
                df_integ.at[idx, "STATUS_RENDIMENTO"] = "SEM_INFORMACAO_OU_NAO_OFERTADO"

        # Ajuste status IDEB
        if pd.isna(row["STATUS_IDEB"]):
            if ano not in anos_com_ideb:
                df_integ.at[idx, "STATUS_IDEB"] = "SEM_EDICAO_IDEB_ANO_PAR_OU_INTERMEDIARIO"
            else:
                df_integ.at[idx, "STATUS_IDEB"] = "SEM_PARTICIPACAO"

    # Padronização de Nomes das Colunas Conforme Especificação Mínima
    df_integ = df_integ.rename(columns={
        "civico_militar": "status_ccm",
        "ETAPA": "etapa_ensino",
        "SAEB_PORTUGUES": "saeb_portugues",
        "SAEB_MATEMATICA": "saeb_matematica",
        "SAEB_NOTA_MEDIA": "saeb_nota_media",
        "STATUS_PARTICIPACAO_SAEB": "status_participacao_saeb",
        "TAXA_APROVACAO": "taxa_aprovacao",
        "TAXA_REPROVACAO": "taxa_reprovacao",
        "TAXA_ABANDONO": "taxa_abandono",
        "STATUS_RENDIMENTO": "status_rendimento",
        "IDEB_OBSERVADO": "ideb_observado",
        "IDEB_META": "ideb_meta",
        "IDEB_COMPONENTE_N": "ideb_componente_n",
        "IDEB_COMPONENTE_P": "ideb_componente_p",
        "TAXA_APROVACAO_IDEB": "taxa_aprovacao_ideb",
        "STATUS_IDEB": "status_ideb"
    })

    # Remover coluna de taxa de aprovação duplicada do SAEB se existir
    cols_to_drop = [c for c in ["TAXA_APROVACAO_x", "TAXA_APROVACAO_y", "IDEB_OBSERVADO_x", "IDEB_OBSERVADO_y", "INDICADOR_RENDIMENTO"] if c in df_integ.columns]
    if cols_to_drop:
        df_integ = df_integ.drop(columns=cols_to_drop)

    # Ordenar logicamente
    df_integ = df_integ.sort_values(by=["codigo_inep", "etapa_ensino", "ano"]).reset_index(drop=True)

    path_matriz_parquet = proc_dir / "ccm_saeb_rendimento_ideb.parquet"
    path_matriz_csv = proc_dir / "ccm_saeb_rendimento_ideb.csv"

    df_integ.to_parquet(path_matriz_parquet, index=False)
    df_integ.to_csv(path_matriz_csv, sep=";", index=False, encoding="utf-8")

    print(f"\nMatriz Integrada Preliminar (2020-2026) gerada com sucesso!")
    print(f"  Parquet: {path_matriz_parquet} ({len(df_integ)} registros)")
    print(f"  CSV: {path_matriz_csv}")

    # 4. Construção da Série Histórica Longitudinal Completa (2005 a 2025)
    # Partir de df_ideb expandido para escolas CCM
    sub_ideb_all = df_ideb[df_ideb["ID_ESCOLA"].isin(ccm_ineps)].copy()
    sub_rend_all = df_rend[df_rend["ID_ESCOLA"].isin(ccm_ineps)].copy()

    # Base longitudinal: união de anos
    df_serie = pd.merge(
        sub_ideb_all,
        sub_rend_all[[
            "ID_ESCOLA", "ANO", "ETAPA",
            "TAXA_APROVACAO", "TAXA_REPROVACAO", "TAXA_ABANDONO", "STATUS_RENDIMENTO"
        ]],
        left_on=["ID_ESCOLA", "ANO_IDEB", "ETAPA"],
        right_on=["ID_ESCOLA", "ANO", "ETAPA"],
        how="outer"
    )

    # Preencher ano
    df_serie["ano"] = df_serie["ANO_IDEB"].combine_first(df_serie["ANO"]).astype(int)
    df_serie = df_serie.drop(columns=["ANO_IDEB", "ANO"])

    # Associar dados cadastrais e ano_inicio_ccm da matriz CCM
    map_inicio = df_ccm_ano.drop_duplicates("codigo_inep").set_index("codigo_inep")["ano_inicio_ccm"].to_dict()
    map_nome = df_mt.set_index("codigo_inep")["nome_escola_cadastro"].to_dict()
    map_mun = df_mt.set_index("codigo_inep")["municipio_cadastro"].to_dict()

    df_serie["ano_inicio_ccm"] = df_serie["ID_ESCOLA"].map(map_inicio)
    df_serie["nome_escola"] = df_serie["ID_ESCOLA"].map(map_nome)
    df_serie["municipio"] = df_serie["ID_ESCOLA"].map(map_mun)

    df_serie = df_serie.rename(columns={
        "ID_ESCOLA": "codigo_inep",
        "ETAPA": "etapa_ensino",
        "TAXA_APROVACAO": "taxa_aprovacao",
        "TAXA_REPROVACAO": "taxa_reprovacao",
        "TAXA_ABANDONO": "taxa_abandono",
        "STATUS_RENDIMENTO": "status_rendimento",
        "IDEB_OBSERVADO": "ideb_observado",
        "IDEB_META": "ideb_meta",
        "IDEB_COMPONENTE_N": "ideb_componente_n",
        "IDEB_COMPONENTE_P": "ideb_componente_p",
        "TAXA_APROVACAO_IDEB": "taxa_aprovacao_ideb",
        "STATUS_IDEB": "status_ideb"
    })

    df_serie = df_serie.sort_values(by=["codigo_inep", "etapa_ensino", "ano"]).reset_index(drop=True)

    path_serie_parquet = proc_dir / "ccm_saeb_rendimento_ideb_serie_completa.parquet"
    path_serie_csv = proc_dir / "ccm_saeb_rendimento_ideb_serie_completa.csv"

    df_serie.to_parquet(path_serie_parquet, index=False)
    df_serie.to_csv(path_serie_csv, sep=";", index=False, encoding="utf-8")

    print(f"\nSérie Histórica Longitudinal Completa (2005-2025) gerada com sucesso!")
    print(f"  Parquet: {path_serie_parquet} ({len(df_serie)} registros)")
    print(f"  CSV: {path_serie_csv}")

    print("\n=== Integração Concluída com Sucesso! ===")

if __name__ == "__main__":
    run()
