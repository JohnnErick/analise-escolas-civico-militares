import streamlit as st
import pandas as pd
import numpy as np
from modules.charts import (
    make_time_series,
    make_before_after_slope_chart,
    make_delta_distribution_histogram
)

def render_temporal_view(df: pd.DataFrame):
    st.header("📈 Evolução Histórica e Séries Temporais (2005 - 2025)")
    st.markdown(
        """
        Acompanhe a trajetória histórica dos indicadores educacionais no Paraná.
        Esta visão permite examinar os dados **antes** e **depois** da implantação do programa estadual (iniciado em 2021).
        """
    )
    
    st.info(
        """
        ℹ️ **Orientação Metodológica para o Jornalista — Marco Histórico (2021):**  
        O Programa dos Colégios Cívico-Militares do Paraná (SEED-PR) foi regulamentado pela Lei Estadual nº 20.338/2020 e 
        entrou em vigor em **2021**.  
        * **2005 a 2019 (Linha de Base):** As escolas rotuladas como "Cívico-Militar" funcionavam como **escolas estaduais regulares civis**. 
        Os dados desse período são fundamentais para responder: *essas escolas já tinham notas maiores ou menores antes de virarem cívico-militares?*  
        * **2021 a 2023 (Implantação):** Período de vigência do modelo. Permite aferir a aceleração ou desaceleração do desempenho.
        """,
        icon="💡"
    )
    
    col_ind, col_bench, col_etapa_info = st.columns([2, 2, 1])
    with col_ind:
        indicador_escolhido = st.selectbox(
            "Selecione o Indicador para Análise Temporal:",
            options=[
                ("SAEB_NOTA_MEDIA", "SAEB — Nota Média Padronizada (0-10)"),
                ("SAEB_PORTUGUES", "SAEB — Língua Portuguesa (Pontos)"),
                ("SAEB_MATEMATICA", "SAEB — Matemática (Pontos)"),
                ("IDEB_OBSERVADO", "IDEB Observado (0-10)"),
                ("TAXA_APROVACAO", "Taxa de Aprovação (%)"),
                ("INDICADOR_RENDIMENTO", "Indicador de Rendimento (0 a 1)"),
            ],
            format_func=lambda x: x[1]
        )
    with col_bench:
        benchmark_temporal = st.selectbox(
            "Grupo de Comparação (Benchmark):",
            options=[
                "Rede Estadual Regular (Não CM)",
                "Não Cívico-Militar (Geral)",
                "Mesmo Município (Pareamento Territorial)"
            ],
            index=0,
            help="Rede Estadual Regular: compara exclusivamente com colégios estaduais da SEED-PR."
        )
    with col_etapa_info:
        st.info("💡 Dica: Isole uma Etapa na barra lateral para acompanhar o ciclo contínuo.")
        
    metric_col, metric_label = indicador_escolhido
    
    # Prepara dataframe com o benchmark selecionado
    if benchmark_temporal == "Rede Estadual Regular (Não CM)":
        cm_part = df[df["TIPO_GESTAO"] == "Cívico-Militar"].copy()
        cm_part["GRUPO_COMPARA"] = "Cívico-Militar"
        ncm_part = df[(df["TIPO_GESTAO"] == "Não Cívico-Militar") & (df["REDE"] == "Estadual")].copy()
        ncm_part["GRUPO_COMPARA"] = "Rede Estadual Regular"
        df_plot = pd.concat([cm_part, ncm_part], ignore_index=True)
        bench_col_name = "Rede Estadual Regular"
    elif benchmark_temporal == "Mesmo Município (Pareamento Territorial)":
        cm_part = df[df["TIPO_GESTAO"] == "Cívico-Militar"].copy()
        cm_cities = cm_part["NO_MUNICIPIO"].dropna().unique()
        cm_part["GRUPO_COMPARA"] = "Cívico-Militar"
        ncm_part = df[(df["TIPO_GESTAO"] == "Não Cívico-Militar") & (df["NO_MUNICIPIO"].isin(cm_cities))].copy()
        ncm_part["GRUPO_COMPARA"] = "Mesmo Município (Não-CM)"
        df_plot = pd.concat([cm_part, ncm_part], ignore_index=True)
        bench_col_name = "Mesmo Município (Não-CM)"
    else:
        df_plot = df[df["TIPO_GESTAO"].isin(["Cívico-Militar", "Não Cívico-Militar"])].copy()
        df_plot["GRUPO_COMPARA"] = df_plot["TIPO_GESTAO"]
        bench_col_name = "Não Cívico-Militar"
    
    # 1. Gráfico de Série Histórica
    fig_temporal = make_time_series(
        df_plot,
        metric_col,
        f"Evolução Temporal: {metric_label} ({benchmark_temporal})",
        metric_label,
        group_col="GRUPO_COMPARA"
    )
    
    if fig_temporal:
        st.plotly_chart(fig_temporal, use_container_width=True)
    else:
        st.warning("Não há dados temporais suficientes para a métrica e filtros selecionados.")
        
    st.markdown("##### Tabela de Trajetória Histórica das Médias")
    df_valid = df_plot.dropna(subset=[metric_col, "GRUPO_COMPARA", "ANO"])
    if not df_valid.empty:
        pivot = df_valid.pivot_table(
            index="ANO",
            columns="GRUPO_COMPARA",
            values=metric_col,
            aggfunc=["mean", "count"]
        )
        if ("mean", "Cívico-Militar") in pivot.columns and ("mean", bench_col_name) in pivot.columns:
            pivot_display = pd.DataFrame(index=pivot.index)
            pivot_display["Média Cívico-Militar"] = pivot[("mean", "Cívico-Militar")]
            pivot_display["Escolas CM"] = pivot[("count", "Cívico-Militar")]
            pivot_display[f"Média {bench_col_name}"] = pivot[("mean", bench_col_name)]
            pivot_display[f"Escolas {bench_col_name}"] = pivot[("count", bench_col_name)]
            pivot_display[f"Diferença (CM - {bench_col_name})"] = pivot_display["Média Cívico-Militar"] - pivot_display[f"Média {bench_col_name}"]
            
            fmt_dict = {
                "Média Cívico-Militar": "{:.2f}",
                "Escolas CM": "{:,.0f}",
                f"Média {bench_col_name}": "{:.2f}",
                f"Escolas {bench_col_name}": "{:,.0f}",
                f"Diferença (CM - {bench_col_name})": "{:+.2f}"
            }
            st.dataframe(
                pivot_display.style.format(fmt_dict),
                use_container_width=True
            )
        else:
            st.dataframe(pivot, use_container_width=True)

    # ==========================================
    # 2. ANÁLISE CONTRAFACTUAL: ANTES VS DEPOIS
    # ==========================================
    st.markdown("---")
    st.subheader("⚖️ Análise de Trajetória: Antes vs Depois da Militarização")
    st.markdown(
        r"""
        Para responder se os colégios militarizados **avançaram em ritmo diferente** do restante da rede, 
        esta análise isola as escolas que possuem registros válidos no período **Pré-Programa (Linha de Base)** 
        e no período **Pós-Programa**, calculando o ganho ou perda real ($\Delta$).
        """
    )
    
    c_ano_pre, c_ano_pos, c_espaco = st.columns([2, 2, 2])
    with c_ano_pre:
        ano_pre = st.selectbox(
            "Ciclo Pré-Programa (Linha de Base):",
            options=[2019, 2017],
            index=0,
            help="2019 é o último ciclo completo antes da vigência do modelo militar."
        )
    with c_ano_pos:
        ano_pos = st.selectbox(
            "Ciclo Pós-Programa (Efetivação):",
            options=[2023, 2021],
            index=0,
            help="2023 representa o ciclo com o programa plenamente implementado."
        )
        
    df_paired = df_plot[df_plot["ANO"].isin([ano_pre, ano_pos])].dropna(subset=[metric_col, "GRUPO_COMPARA", "ID_ESCOLA"])
    pivot_paired = df_paired.pivot_table(index=["ID_ESCOLA", "GRUPO_COMPARA"], columns="ANO", values=metric_col).dropna()
    
    if ano_pre in pivot_paired.columns and ano_pos in pivot_paired.columns and not pivot_paired.empty:
        pivot_paired["DELTA"] = pivot_paired[ano_pos] - pivot_paired[ano_pre]
        df_deltas = pivot_paired.reset_index()
        
        delta_cm = df_deltas[df_deltas["GRUPO_COMPARA"] == "Cívico-Militar"]["DELTA"]
        delta_bench = df_deltas[df_deltas["GRUPO_COMPARA"] == bench_col_name]["DELTA"]
        
        mean_d_cm = delta_cm.mean() if len(delta_cm) > 0 else np.nan
        mean_d_bench = delta_bench.mean() if len(delta_bench) > 0 else np.nan
        did = (mean_d_cm - mean_d_bench) if (pd.notna(mean_d_cm) and pd.notna(mean_d_bench)) else np.nan
        
        # KPIs da Trajetória (Diferença em Diferenças)
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.metric(
                label=f"Variação Média CM ({ano_pre} ➔ {ano_pos})",
                value=f"{mean_d_cm:+.2f}" if pd.notna(mean_d_cm) else "-",
                help=f"Mediana: {delta_cm.median():+.2f}"
            )
            st.caption(f"Amostra: **{len(delta_cm):,}** escolas com pares")
        with k2:
            st.metric(
                label=f"Variação {bench_col_name} ({ano_pre} ➔ {ano_pos})",
                value=f"{mean_d_bench:+.2f}" if pd.notna(mean_d_bench) else "-",
                help=f"Mediana: {delta_bench.median():+.2f}"
            )
            st.caption(f"Amostra: **{len(delta_bench):,}** escolas com pares")
        with k3:
            did_str = f"{did:+.2f}" if pd.notna(did) else "-"
            st.metric(
                label="Diferença de Trajetória (DiD)",
                value=did_str,
                delta=did_str if pd.notna(did) else None,
                delta_color="off"
            )
            st.caption("Δ Cívico-Militar menos Δ Benchmark")
        with k4:
            cm_melhoraram = (delta_cm > 0).sum()
            pct_cm_melh = (cm_melhoraram / len(delta_cm)) * 100 if len(delta_cm) > 0 else 0
            st.metric(
                label="% Escolas CM com Ganho Real",
                value=f"{pct_cm_melh:.1f}%",
                help=f"{cm_melhoraram} de {len(delta_cm)} escolas subiram de nota"
            )
            st.caption(f"**{cm_melhoraram}** de {len(delta_cm)} escolas avançaram")
            
        # Gráficos da Trajetória
        col_g_slope, col_g_hist = st.columns(2)
        with col_g_slope:
            fig_slope = make_before_after_slope_chart(
                df_plot,
                metric_col,
                metric_label,
                year_before=ano_pre,
                year_after=ano_pos,
                group_col="GRUPO_COMPARA",
                title=f"Inclinação da Trajetória Média ({ano_pre} vs {ano_pos})"
            )
            if fig_slope:
                st.plotly_chart(fig_slope, use_container_width=True)
                
        with col_g_hist:
            fig_d_hist = make_delta_distribution_histogram(
                df_plot,
                metric_col,
                metric_label,
                year_before=ano_pre,
                year_after=ano_pos,
                group_col="GRUPO_COMPARA",
                title=f"Distribuição do Ganho/Perda Individual (Δ por Escola)"
            )
            if fig_d_hist:
                st.plotly_chart(fig_d_hist, use_container_width=True)
                
        # Destaques jornalísticos
        st.markdown(
            f"""
            > [!TIP]
            > **Leitura Investigativa dos Resultados ({ano_pre} a {ano_pos}):**  
            > - **Ponto de Partida ({ano_pre}):** No ciclo de {ano_pre}, antes da transição, o grupo que viria a ser Cívico-Militar tinha média de **{pivot_paired[ano_pre].loc[df_deltas[df_deltas['GRUPO_COMPARA']=='Cívico-Militar']['ID_ESCOLA']].mean():.2f}**, contra **{pivot_paired[ano_pre].loc[df_deltas[df_deltas['GRUPO_COMPARA']==bench_col_name]['ID_ESCOLA']].mean():.2f}** do grupo {bench_col_name}.  
            > - **Evolução:** Entre {ano_pre} e {ano_pos}, o grupo Cívico-Militar variou **{mean_d_cm:+.2f}**, enquanto o grupo {bench_col_name} variou **{mean_d_bench:+.2f}**.  
            > - **Diferença Líquida de Ritmo:** A trajetória das cívico-militares foi **{did:+.2f} pontos** em relação ao grupo de controle.
            """
        )
    else:
        st.info("Não há escolas com dados pareados suficientes nos dois anos selecionados para o filtro atual.")
