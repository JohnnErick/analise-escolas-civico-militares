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
    
    col_ind, col_etapa_info = st.columns([2, 1])
    with col_ind:
        indicador_escolhido = st.selectbox(
            "Selecione o Indicador para Análise Temporal:",
            options=[
                ("SAEB_PORTUGUES", "SAEB — Língua Portuguesa (Pontos)"),
                ("SAEB_MATEMATICA", "SAEB — Matemática (Pontos)"),
                ("SAEB_NOTA_MEDIA", "SAEB — Nota Média Padronizada (0-10)"),
                ("IDEB_OBSERVADO", "IDEB Observado (0-10)"),
                ("TAXA_APROVACAO", "Taxa de Aprovação (%)"),
                ("INDICADOR_RENDIMENTO", "Indicador de Rendimento (0 a 1)"),
            ],
            format_func=lambda x: x[1]
        )
    with col_etapa_info:
        st.info("💡 Dica: Use os filtros da barra lateral para isolar uma Etapa de Ensino específica (ex: Anos Finais ou Ensino Médio).")
        
    metric_col, metric_label = indicador_escolhido
    
    fig_temporal = make_time_series(
        df,
        metric_col,
        f"Evolução Temporal: {metric_label}",
        metric_label
    )
    
    if fig_temporal:
        st.plotly_chart(fig_temporal, use_container_width=True)
    else:
        st.warning("Não há dados temporais suficientes para a métrica e filtros selecionados.")
        
    st.markdown("##### Tabela de Trajetória Histórica das Médias")
    df_valid = df.dropna(subset=[metric_col, "TIPO_GESTAO", "ANO"])
    if not df_valid.empty:
        pivot = df_valid.pivot_table(
            index="ANO",
            columns="TIPO_GESTAO",
            values=metric_col,
            aggfunc=["mean", "count"]
        )
        # Formatação limpa
        if ("mean", "Cívico-Militar") in pivot.columns and ("mean", "Não Cívico-Militar") in pivot.columns:
            pivot_display = pd.DataFrame(index=pivot.index)
            pivot_display["Média Cívico-Militar"] = pivot[("mean", "Cívico-Militar")]
            pivot_display["Escolas CM"] = pivot[("count", "Cívico-Militar")]
            pivot_display["Média Não CM"] = pivot[("mean", "Não Cívico-Militar")]
            pivot_display["Escolas Não CM"] = pivot[("count", "Não Cívico-Militar")]
            pivot_display["Diferença (CM - Não CM)"] = pivot_display["Média Cívico-Militar"] - pivot_display["Média Não CM"]
            
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
