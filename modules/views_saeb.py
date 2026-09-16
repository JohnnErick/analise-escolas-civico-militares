import streamlit as st
import pandas as pd
from modules.components import render_kpi_cards, render_stats_table
from modules.charts import make_boxplot_comparison, make_histogram_comparison, make_scatter_disciplinas

def render_saeb_view(df: pd.DataFrame):
    st.header("🎯 Indicador Principal: SAEB (Sistema de Avaliação da Educação Básica)")
    st.markdown(
        """
        O SAEB afere o rendimento e a aprendizagem dos estudantes através de testes padronizados. 
        Abaixo, você pode explorar as proficiências em **Língua Portuguesa** e **Matemática** 
        (na escala de proficiência do SAEB, tipicamente entre 150 e 400 pontos) e a **Nota Média Padronizada** (escala de 0 a 10).
        """
    )
    
    tab_port, tab_mat, tab_media, tab_relacao = st.tabs([
        "📖 Língua Portuguesa",
        "📐 Matemática",
        "⭐ Nota Média SAEB (0-10)",
        "⚖️ Relação Português vs Matemática"
    ])
    
    with tab_port:
        st.subheader("Proficiência SAEB — Língua Portuguesa")
        render_kpi_cards(df, "SAEB_PORTUGUES", "Língua Portuguesa", format_str="{:.1f}")
        
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            fig_box = make_boxplot_comparison(
                df, "SAEB_PORTUGUES",
                "Distribuição das Notas — Língua Portuguesa",
                "Proficiência SAEB (Pontos)"
            )
            if fig_box:
                st.plotly_chart(fig_box, use_container_width=True)
            else:
                st.info("Sem dados suficientes para gerar o boxplot.")
                
        with col_g2:
            fig_hist = make_histogram_comparison(
                df, "SAEB_PORTUGUES",
                "Histograma e Densidade — Língua Portuguesa",
                "Proficiência SAEB (Pontos)"
            )
            if fig_hist:
                st.plotly_chart(fig_hist, use_container_width=True)
            else:
                st.info("Sem dados suficientes para o histograma.")
                
        render_stats_table(df, "SAEB_PORTUGUES", "Língua Portuguesa")
        
    with tab_mat:
        st.subheader("Proficiência SAEB — Matemática")
        render_kpi_cards(df, "SAEB_MATEMATICA", "Matemática", format_str="{:.1f}")
        
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            fig_box = make_boxplot_comparison(
                df, "SAEB_MATEMATICA",
                "Distribuição das Notas — Matemática",
                "Proficiência SAEB (Pontos)"
            )
            if fig_box:
                st.plotly_chart(fig_box, use_container_width=True)
            else:
                st.info("Sem dados suficientes para gerar o boxplot.")
                
        with col_g2:
            fig_hist = make_histogram_comparison(
                df, "SAEB_MATEMATICA",
                "Histograma e Densidade — Matemática",
                "Proficiência SAEB (Pontos)"
            )
            if fig_hist:
                st.plotly_chart(fig_hist, use_container_width=True)
            else:
                st.info("Sem dados suficientes para o histograma.")
                
        render_stats_table(df, "SAEB_MATEMATICA", "Matemática")
        
    with tab_media:
        st.subheader("Nota Média Padronizada do SAEB (Escala 0 a 10)")
        st.markdown(
            "Esta é a nota padronizada calculada pelo INEP a partir do desempenho em Matemática e Língua Portuguesa (fator $N$ do IDEB)."
        )
        render_kpi_cards(df, "SAEB_NOTA_MEDIA", "Nota Média SAEB", format_str="{:.2f}")
        
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            fig_box = make_boxplot_comparison(
                df, "SAEB_NOTA_MEDIA",
                "Distribuição da Nota Média Padronizada",
                "Nota Padronizada (0 a 10)"
            )
            if fig_box:
                st.plotly_chart(fig_box, use_container_width=True)
        with col_g2:
            fig_hist = make_histogram_comparison(
                df, "SAEB_NOTA_MEDIA",
                "Histograma da Nota Média Padronizada",
                "Nota Padronizada (0 a 10)"
            )
            if fig_hist:
                st.plotly_chart(fig_hist, use_container_width=True)
                
        render_stats_table(df, "SAEB_NOTA_MEDIA", "Nota Média SAEB")
        
    with tab_relacao:
        st.subheader("Correlação entre Desempenho em Português e Matemática")
        st.markdown(
            "Cada ponto representa uma escola. As linhas tracejadas marcam a média geral de cada disciplina. Permite identificar se o desempenho de um grupo é equilibrado ou assimétrico entre as áreas."
        )
        fig_scatter = make_scatter_disciplinas(df, "SAEB: Língua Portuguesa vs Matemática por Escola")
        if fig_scatter:
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.info("Sem dados suficientes para o gráfico de dispersão.")
