import streamlit as st
import pandas as pd
from modules.charts import make_time_series

def render_temporal_view(df: pd.DataFrame):
    st.header("📈 Evolução Histórica e Séries Temporais (2005 - 2025)")
    st.markdown(
        """
        Acompanhe a trajetória histórica dos indicadores ano a ano.
        Esta visão é essencial para verificar o comportamento das escolas **antes** e **depois** 
        dos programas de militarização (iniciados gradualmente no Paraná a partir de 2020/2021).
        """
    )
    
    col_ind, col_bench, col_etapa_info = st.columns([2, 2, 1])
    with col_ind:
        indicador_escolhido = st.selectbox(
            "Selecione o Indicador para Análise Temporal:",
            options=[
                ("TAXA_APROVACAO", "Taxa de Aprovação (%)"),
                ("SAEB_PORTUGUES", "SAEB — Língua Portuguesa (Pontos)"),
                ("SAEB_MATEMATICA", "SAEB — Matemática (Pontos)"),
                ("SAEB_NOTA_MEDIA", "SAEB — Nota Média Padronizada (0-10)"),
                ("IDEB_OBSERVADO", "IDEB Observado (0-10)"),
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
            index=0
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
        # Formatação limpa
        if ("mean", "Cívico-Militar") in pivot.columns and ("mean", bench_col_name) in pivot.columns:
            pivot_display = pd.DataFrame(index=pivot.index)
            pivot_display["Média Cívico-Militar"] = pivot[("mean", "Cívico-Militar")]
            pivot_display["Escolas CM"] = pivot[("count", "Cívico-Militar")]
            pivot_display[f"Média {bench_col_name}"] = pivot[("mean", bench_col_name)]
            pivot_display[f"Escolas {bench_col_name}"] = pivot[("count", bench_col_name)]
            pivot_display[f"Diferença (CM - {bench_col_name})"] = pivot_display["Média Cívico-Militar"] - pivot_display[f"Média {bench_col_name}"]
            
            st.dataframe(
                pivot_display.style.format({
                    "Média Cívico-Militar": "{:.2f}",
                    "Escolas CM": "{:,.0f}",
                    "Média Não CM": "{:.2f}",
                    "Escolas Não CM": "{:,.0f}",
                    "Diferença (CM - Não CM)": "{:+.2f}"
                }),
                use_container_width=True
            )
        else:
            st.dataframe(pivot, use_container_width=True)
