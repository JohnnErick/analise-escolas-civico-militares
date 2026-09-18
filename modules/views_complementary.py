import streamlit as st
import pandas as pd
from modules.components import render_kpi_cards, render_stats_table
from modules.charts import (
    make_boxplot_comparison,
    make_histogram_comparison,
    make_ideb_vs_projecao_scatter,
    make_grade_approval_bars,
    make_approval_brackets_bar,
    make_scatter_aprovacao_vs_saeb
)

def render_complementary_view(df: pd.DataFrame):
    st.header("📊 Indicadores Complementares: IDEB e Rendimento Escolar")
    st.markdown(
        """
        O IDEB combina o desempenho no SAEB ($N$) com a taxa de aprovação/rendimento ($P$), 
        segundo a fórmula $IDEB = N \\times P$. 
        Esta seção contextualiza o desempenho global das unidades escolares.
        """
    )
    
    st.warning(
        """
        ⚠️ **Transparência sobre Taxas de Rendimento:**  
        Conforme verificado diretamente na base oficial fornecida pelo INEP/MEC (`divulgacao_pr_consolidado.xlsx`), 
        estão presentes as taxas de **Aprovação** e o **Indicador de Rendimento escolar**. 
        **Não constam** nesta base colunas específicas de taxas de reprovação e abandono escolar.
        """,
        icon="ℹ️"
    )
    
    tab_ideb, tab_metas, tab_aprov = st.tabs([
        "🏆 IDEB Observado",
        "🎯 Atingimento de Metas (Projeção INEP)",
        "📋 Taxa de Aprovação e Rendimento"
    ])
    
    with tab_ideb:
        st.subheader("IDEB Observado (Escala 0 a 10)")
        render_kpi_cards(df, "IDEB_OBSERVADO", "IDEB", format_str="{:.2f}")
        
        c1, c2 = st.columns(2)
        with c1:
            fig_box = make_boxplot_comparison(
                df, "IDEB_OBSERVADO",
                "Distribuição do IDEB Observado",
                "IDEB (0 a 10)"
            )
            if fig_box:
                st.plotly_chart(fig_box, use_container_width=True)
        with c2:
            fig_hist = make_histogram_comparison(
                df, "IDEB_OBSERVADO",
                "Histograma do IDEB Observado",
                "IDEB (0 a 10)"
            )
            if fig_hist:
                st.plotly_chart(fig_hist, use_container_width=True)
                
        render_stats_table(df, "IDEB_OBSERVADO", "IDEB Observado")
        
    with tab_metas:
        st.subheader("Relação entre IDEB Observado e Projeção Oficial")
        st.markdown(
            "Pontos acima da linha tracejada indicam escolas que **superaram a meta** estabelecida pelo Ministério da Educação."
        )
        fig_meta = make_ideb_vs_projecao_scatter(df, "IDEB Observado vs Meta Projetada pelo INEP")
        if fig_meta:
            st.plotly_chart(fig_meta, use_container_width=True)
        else:
            st.info("Não há dados de projeção para o ano/etapa selecionados.")
            
        # Estatística de % de cumprimento de meta
        df_proj = df.dropna(subset=["IDEB_OBSERVADO", "IDEB_PROJECAO", "TIPO_GESTAO"])
        if not df_proj.empty:
            df_proj["ATINGIU"] = df_proj["IDEB_OBSERVADO"] >= df_proj["IDEB_PROJECAO"]
            meta_resumo = df_proj.groupby("TIPO_GESTAO")["ATINGIU"].agg(
                Total="count",
                Atingiram="sum",
                Percentual=lambda x: (x.sum() / len(x)) * 100
            ).reset_index()
            st.markdown("##### Percentual de Escolas que Cumpriram a Meta do IDEB")
            st.dataframe(
                meta_resumo.style.format({
                    "Total": "{:,}",
                    "Atingiram": "{:,}",
                    "Percentual": "{:.1f}%"
                }),
                use_container_width=True,
                hide_index=True
            )
            
    with tab_aprov:
        st.subheader("Taxa de Aprovação Escolar (%)")
        render_kpi_cards(df, "TAXA_APROVACAO", "Taxa de Aprovação", format_str="{:.1f}%")
        
        c1, c2 = st.columns(2)
        with c1:
            fig_box = make_boxplot_comparison(
                df, "TAXA_APROVACAO",
                "Distribuição da Taxa de Aprovação (%)",
                "Aprovação (%)"
            )
            if fig_box:
                st.plotly_chart(fig_box, use_container_width=True)
        with c2:
            fig_box_rend = make_boxplot_comparison(
                df, "INDICADOR_RENDIMENTO",
                "Distribuição do Indicador de Rendimento (0 a 1)",
                "Indicador de Rendimento (P)"
            )
            if fig_box_rend:
                st.plotly_chart(fig_box_rend, use_container_width=True)
                
        # Faixas de Aprovação e Comparativo por Série
        c_faixa, c_serie = st.columns(2)
        with c_faixa:
            fig_faixas = make_approval_brackets_bar(df, title="Proporção de Escolas por Faixa de Aprovação (%)")
            if fig_faixas:
                st.plotly_chart(fig_faixas, use_container_width=True)
        with c_serie:
            fig_series = make_grade_approval_bars(df, title="Taxa Média de Aprovação por Série/Ano Escolar")
            if fig_series:
                st.plotly_chart(fig_series, use_container_width=True)
                
        # Cruzamento: Taxa de Aprovação vs SAEB
        st.markdown("##### Relação entre Taxa de Aprovação e Nota SAEB")
        fig_cross = make_scatter_aprovacao_vs_saeb(
            df,
            saeb_col="SAEB_NOTA_MEDIA",
            saeb_label="Nota Média SAEB (0-10)",
            title="Dispersão: Taxa de Aprovação vs Nota Média SAEB"
        )
        if fig_cross:
            st.plotly_chart(fig_cross, use_container_width=True)
                
        render_stats_table(df, "TAXA_APROVACAO", "Taxa de Aprovação (%)")
