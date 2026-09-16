import streamlit as st
import pandas as pd
from modules.charts import make_city_comparison_bar, make_school_map

def render_geo_view(df: pd.DataFrame):
    st.header("🗺️ Análise Comparativa por Município e Território")
    st.markdown(
        """
        Para isolar fatores socioeconômicos regionais e territoriais, esta visão apresenta a 
        distribuição espacial das escolas e compara o desempenho entre escolas **Cívico-Militares** 
        e **Não Cívico-Militares** dentro dos mesmos municípios.
        """
    )
    
    col_ind, col_filt, col_top = st.columns([2, 2, 1])
    with col_ind:
        indicador_geo = st.selectbox(
            "Métrica para Comparação:",
            options=[
                ("SAEB_NOTA_MEDIA", "SAEB — Nota Média (0-10)"),
                ("SAEB_MATEMATICA", "SAEB — Matemática"),
                ("SAEB_PORTUGUES", "SAEB — Língua Portuguesa"),
                ("IDEB_OBSERVADO", "IDEB Observado"),
                ("TAXA_APROVACAO", "Taxa de Aprovação (%)")
            ],
            format_func=lambda x: x[1]
        )
    with col_filt:
        modo_mapa = st.selectbox(
            "Escolas Exibidas no Mapa:",
            options=[
                "Apenas Municípios com Cívico-Militares",
                "Apenas Cívico-Militares (Pontos Exatos KML)",
                "Todas as Escolas da Amostra Filtrada"
            ]
        )
    with col_top:
        top_n = st.slider("Top Municípios no Gráfico:", min_value=5, max_value=40, value=15, step=5)
        
    metric_col, metric_label = indicador_geo

    # 1. Seção do Mapa Interativo
    st.markdown("##### 📍 Distribuição Territorial das Escolas (KML Georreferenciado)")
    st.caption("As escolas cívico-militares possuem coordenadas geográficas exatas auditadas a partir do arquivo KML oficial da SEED-PR.")

    # Filtro de dados para o mapa
    cm_cities = df[df["TIPO_GESTAO"] == "Cívico-Militar"]["NO_MUNICIPIO"].dropna().unique()
    if modo_mapa == "Apenas Cívico-Militares (Pontos Exatos KML)":
        df_mapa = df[df["TIPO_GESTAO"] == "Cívico-Militar"]
    elif modo_mapa == "Apenas Municípios com Cívico-Militares":
        df_mapa = df[df["NO_MUNICIPIO"].isin(cm_cities)]
    else:
        df_mapa = df

    fig_map = make_school_map(
        df_mapa,
        metric_col,
        metric_label,
        f"Distribuição Geográfica: {metric_label}"
    )
    if fig_map:
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("Não há coordenadas disponíveis para os filtros selecionados.")

    st.markdown("---")

    # 2. Seção do Gráfico de Barras Comparativo
    fig_city = make_city_comparison_bar(
        df,
        metric_col,
        f"Comparativo Municipal: {metric_label} (Municípios com presença Cívico-Militar)",
        metric_label,
        top_n=top_n
    )
    
    if fig_city:
        st.plotly_chart(fig_city, use_container_width=True)
    else:
        st.info("Não há dados municipais suficientes para o gráfico nos filtros selecionados.")
        
    st.markdown("##### Tabela Comparativa Detalhada por Município")
    # Filtra municípios com escolas cívico-militares
    df_cm_cities = df[df["NO_MUNICIPIO"].isin(cm_cities)].dropna(subset=[metric_col, "TIPO_GESTAO"])
    
    if not df_cm_cities.empty:
        pivot_city = df_cm_cities.pivot_table(
            index="NO_MUNICIPIO",
            columns="TIPO_GESTAO",
            values=metric_col,
            aggfunc=["mean", "count"]
        )
        if ("mean", "Cívico-Militar") in pivot_city.columns and ("mean", "Não Cívico-Militar") in pivot_city.columns:
            df_table = pd.DataFrame(index=pivot_city.index)
            df_table["Média CM"] = pivot_city[("mean", "Cívico-Militar")]
            df_table["Escolas CM"] = pivot_city[("count", "Cívico-Militar")]
            df_table["Média Não-CM"] = pivot_city[("mean", "Não Cívico-Militar")]
            df_table["Escolas Não-CM"] = pivot_city[("count", "Não Cívico-Militar")]
            df_table["Diferença (CM - Não-CM)"] = df_table["Média CM"] - df_table["Média Não-CM"]
            
            # Ordenar por diferença
            df_table = df_table.dropna(subset=["Média CM", "Média Não-CM"]).sort_values("Diferença (CM - Não-CM)", ascending=False)
            
            styler = df_table.style.format({
                "Média CM": "{:.2f}",
                "Escolas CM": "{:,.0f}",
                "Média Não-CM": "{:.2f}",
                "Escolas Não-CM": "{:,.0f}",
                "Diferença (CM - Não-CM)": "{:+.2f}"
            })
            try:
                styler = styler.background_gradient(subset=["Diferença (CM - Não-CM)"], cmap="coolwarm", vmin=-10, vmax=10)
            except Exception:
                pass

            st.dataframe(
                styler,
                use_container_width=True
            )
