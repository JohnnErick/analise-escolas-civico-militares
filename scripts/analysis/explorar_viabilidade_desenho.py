#!/usr/bin/env python3
"""
explorar_viabilidade_desenho.py

Script exploratório para avaliar a viabilidade metodológica dos desenhos estatísticos
(Diferenças-em-Diferenças, Pareamento por Escore de Propensão, Séries Temporais)
para a investigação dos Colégios Cívico-Militares do Paraná.

Examina:
1. Estrutura temporal dos dados disponíveis (pré vs. pós);
2. Tamanho dos grupos (Tratamento 2024, Futuro 2026, Consultadas Rejeitadas, Controles Regulares);
3. Disponibilidade de observações por etapa de ensino;
4. Balanço de linha de base (baseline balance 2017–2023);
5. Tendências prévias (teste de tendências paralelas pré-intervenção);
6. Suporte comum (overlap) para pareamento.
"""

from pathlib import Path
import pandas as pd
import numpy as np

def run():
    print("=== Iniciando Avaliação Exploratória da Viabilidade do Desenho Estatístico ===")
    base_dir = Path(__file__).resolve().parent.parent.parent
    proc_dir = base_dir / "data" / "processed"

    # Carregar dados
    df_ccm_ano = pd.read_csv(proc_dir / "historico_ccm_por_ano.csv", sep=";")
    df_saeb = pd.read_parquet(proc_dir / "saeb" / "saeb_escolas_parana_tidy.parquet")
    df_rend = pd.read_parquet(proc_dir / "rendimento" / "rendimento_escolas_parana_tidy.parquet")
    df_ideb = pd.read_parquet(proc_dir / "ideb" / "ideb_escolas_parana_tidy.parquet")
    df_mt = pd.read_csv(proc_dir / "historico_ccm_matching_inep.csv", sep=";")

    # Identificar status das escolas auditadas
    unicos_ccm = df_ccm_ano.drop_duplicates("codigo_inep").set_index("codigo_inep")
    map_inicio = unicos_ccm["ano_inicio_ccm"].to_dict()

    print("\n1. Estrutura dos Grupos Auditados (N=201):")
    print(unicos_ccm["ano_inicio_ccm"].value_counts(dropna=False))

    # Definir grupos analíticos:
    # - GRUPO_2024: ano_inicio_ccm == 2024 (106 escolas)
    # - GRUPO_2026: ano_inicio_ccm == 2026 (33 escolas)
    # - GRUPO_CONSULTA_REJEITADA: ano_inicio_ccm == INDETERMINADO (62 escolas)
    # - GRUPO_REGULAR_POOL: escolas estaduais do PR que nunca foram CCM
    todos_ccm_ineps = set(df_mt["codigo_inep"].unique())

    # Universo de escolas estaduais regulares no SAEB e Rendimento
    estaduais_saeb = df_saeb[df_saeb["REDE"] == "Estadual"].copy()
    estaduais_rend = df_rend[df_rend["REDE"].str.contains("Estadual", case=False, na=False)].copy()

    # Adicionar grupo institucional no SAEB
    def classificar_grupo(inep):
        if inep in map_inicio:
            ini = map_inicio[inep]
            if ini == "2024" or ini == 2024:
                return "CCM_2024"
            elif ini == "2026" or ini == 2026:
                return "CCM_2026_FUTURO"
            else:
                return "CCM_CONSULTADA_REJEITADA"
        return "REGULAR_ESTADUAL"

    estaduais_saeb["GRUPO"] = estaduais_saeb["ID_ESCOLA"].apply(classificar_grupo)
    estaduais_rend["GRUPO"] = estaduais_rend["ID_ESCOLA"].apply(classificar_grupo)

    print("\n2. Contagem de Escolas Únicas por Grupo no Cadastro Estadual:")
    print("No SAEB:")
    print(estaduais_saeb.groupby("GRUPO")["ID_ESCOLA"].nunique())
    print("\nNo Rendimento (Censo Escolar):")
    print(estaduais_rend.groupby("GRUPO")["ID_ESCOLA"].nunique())

    # 3. Disponibilidade Temporal de Dados
    print("\n3. Disponibilidade Temporal dos Indicadores:")
    print("Anos SAEB no dataset:", sorted(estaduais_saeb["ANO_SAEB"].unique()))
    print("Anos Rendimento no dataset:", sorted(estaduais_rend["ANO"].unique()))

    # 4. Análise de Linha de Base (Baseline) para Anos Finais (6º ao 9º ano)
    # Comparar o grupo CCM_2024 com REGULAR_ESTADUAL em 2017, 2019, 2021, 2023 (pré-intervenção!)
    af_saeb = estaduais_saeb[estaduais_saeb["ETAPA"] == "Anos Finais (6º-9º)"].copy()
    af_pre = af_saeb[af_saeb["ANO_SAEB"].isin([2017, 2019, 2021, 2023])]

    print("\n4. Trajetória Pré-Intervenção (Baseline) — Anos Finais (Média Matemática):")
    tabela_mat = af_pre.groupby(["ANO_SAEB", "GRUPO"])["SAEB_MATEMATICA"].agg(["count", "mean"]).unstack("GRUPO")
    print(tabela_mat.round(2))

    print("\n5. Trajetória Pré-Intervenção (Baseline) — Anos Finais (Média Português):")
    tabela_port = af_pre.groupby(["ANO_SAEB", "GRUPO"])["SAEB_PORTUGUES"].agg(["count", "mean"]).unstack("GRUPO")
    print(tabela_port.round(2))

    # Análise de Rendimento nos Anos Finais (2017 a 2023)
    af_rend = estaduais_rend[estaduais_rend["ETAPA"] == "Anos Finais (6º-9º)"].copy()
    print("\n6. Trajetória de Fluxo Escolar Pré-Intervenção — Anos Finais (Taxa Média de Aprovação %):")
    tabela_aprov = af_rend.groupby(["ANO", "GRUPO"])["TAXA_APROVACAO"].agg(["count", "mean"]).unstack("GRUPO")
    print(tabela_aprov.round(2))

    print("\n7. Trajetória de Fluxo Escolar Pré-Intervenção — Anos Finais (Taxa Média de Abandono %):")
    tabela_aband = af_rend.groupby(["ANO", "GRUPO"])["TAXA_ABANDONO"].agg(["count", "mean"]).unstack("GRUPO")
    print(tabela_aband.round(2))

    # 8. Análise de Linha de Base para Ensino Médio
    em_saeb = estaduais_saeb[estaduais_saeb["ETAPA"] == "Ensino Médio"].copy()
    em_pre = em_saeb[em_saeb["ANO_SAEB"].isin([2017, 2019, 2021, 2023])]
    print("\n8. Trajetória Pré-Intervenção (Baseline) — Ensino Médio (Média Matemática):")
    tabela_mat_em = em_pre.groupby(["ANO_SAEB", "GRUPO"])["SAEB_MATEMATICA"].agg(["count", "mean"]).unstack("GRUPO")
    print(tabela_mat_em.round(2))

    # 9. Teste de Diferencial de Tendências Prévias (Parallel Trends Check 2017 -> 2023)
    # Variação pré-tratamento 2017 a 2023 nos Anos Finais
    print("\n9. Variação Prévia (2017 para 2023) — Teste de Tendências Paralelas:")
    # Pivotar por escola
    piv_mat = af_pre.pivot_table(index=["ID_ESCOLA", "GRUPO"], columns="ANO_SAEB", values="SAEB_MATEMATICA")
    piv_mat["diff_2017_2023"] = piv_mat[2023] - piv_mat[2017]
    piv_mat["diff_2021_2023"] = piv_mat[2023] - piv_mat[2021]
    print("Variação Média em Matemática (Anos Finais):")
    print(piv_mat.groupby("GRUPO")[["diff_2017_2023", "diff_2021_2023"]].agg(["count", "mean", "std"]).round(2))

    print("\n=== Avaliação Exploratória Concluída! ===")

if __name__ == "__main__":
    run()
