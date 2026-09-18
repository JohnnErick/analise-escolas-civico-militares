import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from modules.components import render_kpi_cards, render_stats_table
from modules.charts import (
    COLOR_MAP,
    make_boxplot_comparison,
    make_histogram_comparison,
    make_scatter_aprovacao_vs_saeb,
    make_grade_approval_bars,
    make_approval_brackets_bar
)

def render_comparisons_view(df: pd.DataFrame, df_raw: pd.DataFrame):
    st.header("⚖️ Central de Comparações & Targets de Investigação")
    st.markdown(
        """
        Esta seção permite comparar o desempenho dos colégios **Cívico-Militares** contra diferentes 
        **grupos de referência (benchmarks)** em qualquer **indicador-alvo (target)** de sua escolha.
        """
    )
    
    # ==========================================
    # BARRA DE SELEÇÃO: TARGET & BENCHMARK
    # ==========================================
    st.markdown("#### 🎯 Configuração do Target de Comparação")
    col_target, col_bench, col_filtro_extra = st.columns([2.2, 2.2, 1.6])
    
    TARGET_OPTIONS = [
        (
            "TAXA_APROVACAO",
            "📋 Taxa de Aprovação Escolar (%)",
            "{:.1f}%",
            "Taxa de Aprovação (%)",
            "Percentual de estudantes promovidos no ano letivo. Comenta-se amplamente no debate educacional sobre taxas de aprovação próximas a 100% e sua relação com proficiências reais em avaliações padronizadas."
        ),
        (
            "TAXA_NAO_APROVACAO",
            "⚠️ Taxa de Não-Aprovação (Reprovação + Abandono %)",
            "{:.1f}%",
            "Não-Aprovação (%)",
            "Percentual de retenção ou evasão (calculado por 100% - Taxa de Aprovação). Como a base de divulgação do IDEB não decompõe reprovação e abandono, este indicador sintetiza o fluxo de interrupção escolar."
        ),
        (
            "SAEB_NOTA_MEDIA",
            "⭐ SAEB — Nota Média Padronizada (0 a 10)",
            "{:.2f}",
            "Nota Média SAEB (0-10)",
            "Nota padronizada calculada pelo INEP com base no rendimento conjunto de Português e Matemática (fator N do IDEB)."
        ),
        (
            "SAEB_PORTUGUES",
            "📖 SAEB — Língua Portuguesa (Pontos)",
            "{:.1f}",
            "Proficiência Língua Portuguesa",
            "Escala de proficiência do SAEB para domínio de leitura e interpretação textual (tipicamente 150 a 400 pontos)."
        ),
        (
            "SAEB_MATEMATICA",
            "📐 SAEB — Matemática (Pontos)",
            "{:.1f}",
            "Proficiência Matemática",
            "Escala de proficiência do SAEB para raciocínio lógico e cálculo matemático."
        ),
        (
            "IDEB_OBSERVADO",
            "🏆 IDEB Observado (0 a 10)",
            "{:.2f}",
            "IDEB Observado",
            "Índice de Desenvolvimento da Educação Básica: sintetiza aprendizagem (SAEB) e fluxo (Aprovação) na fórmula IDEB = N × P."
        ),
        (
            "INDICADOR_RENDIMENTO",
            "📈 Indicador de Rendimento (0 a 1)",
            "{:.3f}",
            "Indicador de Rendimento (P)",
            "Média harmônica das taxas de aprovação nas séries da etapa avaliada."
        ),
        (
            "DELTA_META_IDEB",
            "🎯 Superação da Meta do IDEB (Observado - Projeção)",
            "{:+.2f}",
            "Diferença em relação à Meta",
            "Diferença entre o IDEB obtido pela escola e a meta projetada pelo Ministério da Educação / INEP."
        )
    ]
    
    with col_target:
        idx_target = st.selectbox(
            "Selecione o Target de Comparação (Indicador):",
            options=range(len(TARGET_OPTIONS)),
            format_func=lambda i: TARGET_OPTIONS[i][1],
            index=0,  # Padrão: Taxa de Aprovação conforme pedido pelo usuário
            help="Escolha qual métrica educacional será o centro da comparação."
        )
        
    metric_col, metric_label, format_str, y_axis_label, metric_desc = TARGET_OPTIONS[idx_target]
    
    with col_bench:
        benchmark_choice = st.selectbox(
            "Selecione o Grupo de Comparação (Benchmark Target):",
            options=[
                "Rede Estadual Regular (Não CM)",
                "Não Cívico-Militar (Geral)",
                "Mesmo Município (Pareamento Territorial)"
            ],
            index=0,  # Padrão: Rede Estadual Regular (comparativo mais simétrico e justo)
            help=(
                "Rede Estadual Regular: Compara apenas com escolas estaduais da SEED-PR regulares (exclui municipais/privadas).\n"
                "Mesmo Município: Isola escolas dos municípios onde há unidades cívico-militares ativas."
            )
        )
        
    with col_filtro_extra:
        filtro_amostra = st.selectbox(
            "Filtro de Amostra:",
            options=["Todas as Escolas", "Apenas com Notas SAEB"],
            index=0
        )
        
    # Informações contextuais do target
    st.caption(f"ℹ️ **Sobre este target:** {metric_desc}")
    
    # ==========================================
    # PREPARAÇÃO DOS DADOS DE COMPARAÇÃO
    # ==========================================
    df_work = df.copy()
    
    # Cria coluna calculada de delta de meta se necessário
    if "DELTA_META_IDEB" not in df_work.columns:
        if "IDEB_OBSERVADO" in df_work.columns and "IDEB_PROJECAO" in df_work.columns:
            df_work["DELTA_META_IDEB"] = df_work["IDEB_OBSERVADO"] - df_work["IDEB_PROJECAO"]
        else:
            df_work["DELTA_META_IDEB"] = np.nan
            
    # Cria coluna de Não-Aprovação (100% - Taxa de Aprovação)
    if "TAXA_APROVACAO" in df_work.columns:
        df_work["TAXA_NAO_APROVACAO"] = 100.0 - df_work["TAXA_APROVACAO"]
            
    if filtro_amostra == "Apenas com Notas SAEB":
        df_work = df_work[df_work["SAEB_PORTUGUES"].notna() & df_work["SAEB_MATEMATICA"].notna()]
        
    # Constrói grupos com base na escolha do benchmark
    if benchmark_choice == "Rede Estadual Regular (Não CM)":
        cm_part = df_work[df_work["TIPO_GESTAO"] == "Cívico-Militar"].copy()
        cm_part["GRUPO_COMPARA"] = "Cívico-Militar"
        ncm_part = df_work[(df_work["TIPO_GESTAO"] == "Não Cívico-Militar") & (df_work["REDE"] == "Estadual")].copy()
        ncm_part["GRUPO_COMPARA"] = "Rede Estadual Regular"
        df_comp = pd.concat([cm_part, ncm_part], ignore_index=True)
        bench_label = "Rede Estadual Regular"
        
    elif benchmark_choice == "Mesmo Município (Pareamento Territorial)":
        cm_part = df_work[df_work["TIPO_GESTAO"] == "Cívico-Militar"].copy()
        cm_cities = cm_part["NO_MUNICIPIO"].dropna().unique()
        cm_part["GRUPO_COMPARA"] = "Cívico-Militar"
        ncm_part = df_work[(df_work["TIPO_GESTAO"] == "Não Cívico-Militar") & (df_work["NO_MUNICIPIO"].isin(cm_cities))].copy()
        ncm_part["GRUPO_COMPARA"] = "Mesmo Município (Não-CM)"
        df_comp = pd.concat([cm_part, ncm_part], ignore_index=True)
        bench_label = "Mesmo Município (Não-CM)"
        
    else:  # Não Cívico-Militar (Geral)
        df_comp = df_work[df_work["TIPO_GESTAO"].isin(["Cívico-Militar", "Não Cívico-Militar"])].copy()
        df_comp["GRUPO_COMPARA"] = df_comp["TIPO_GESTAO"]
        bench_label = "Não Cívico-Militar"
        
    df_valid = df_comp.dropna(subset=[metric_col, "GRUPO_COMPARA"])
    
    if df_valid.empty:
        st.warning(f"Não há dados suficientes disponíveis para o indicador '{metric_label}' com os filtros atuais.")
        return
        
    st.markdown("---")
    
    # ==========================================
    # CARTÕES KPI COMPARATIVOS
    # ==========================================
    st.markdown(f"##### 📊 Indicadores Comparativos: **{metric_label}**")
    render_kpi_cards(
        df_comp,
        metric_col=metric_col,
        metric_title=metric_label,
        format_str=format_str,
        group_col="GRUPO_COMPARA",
        cm_group="Cívico-Militar",
        benchmark_group=bench_label
    )
    
    st.markdown("---")
    
    # ==========================================
    # ABAS DE INVESTIGAÇÃO DETALHADA DO TARGET
    # ==========================================
    tab_dist, tab_faixas, tab_cruzamento, tab_series, tab_stats = st.tabs([
        "📊 Distribuição & Dispersão",
        "📑 Faixas & Concentração",
        "⚖️ Relação Aprovação vs SAEB",
        "🏫 Aprovação por Série / Ano",
        "📋 Tabela Descritiva & Rankings"
    ])
    
    with tab_dist:
        st.subheader(f"Distribuição Estatística — {metric_label}")
        st.markdown(
            f"Comparação direta da forma de distribuição dos valores entre **Cívico-Militar** e **{bench_label}**."
        )
        
        c1, c2 = st.columns(2)
        with c1:
            fig_box = make_boxplot_comparison(
                df_comp,
                metric_col,
                f"Boxplot: {metric_label}",
                y_axis_label,
                group_col="GRUPO_COMPARA"
            )
            if fig_box:
                st.plotly_chart(fig_box, use_container_width=True)
            else:
                st.info("Sem dados suficientes para gerar o boxplot.")
                
        with c2:
            fig_hist = make_histogram_comparison(
                df_comp,
                metric_col,
                f"Histograma e Densidade: {metric_label}",
                y_axis_label,
                group_col="GRUPO_COMPARA"
            )
            if fig_hist:
                st.plotly_chart(fig_hist, use_container_width=True)
            else:
                st.info("Sem dados suficientes para gerar o histograma.")
                
        # Destaque de percentis
        p25_cm = df_comp[df_comp["GRUPO_COMPARA"] == "Cívico-Militar"][metric_col].quantile(0.25)
        p75_cm = df_comp[df_comp["GRUPO_COMPARA"] == "Cívico-Militar"][metric_col].quantile(0.75)
        p25_bench = df_comp[df_comp["GRUPO_COMPARA"] == bench_label][metric_col].quantile(0.25)
        p75_bench = df_comp[df_comp["GRUPO_COMPARA"] == bench_label][metric_col].quantile(0.75)
        
        col_p1, col_p2 = st.columns(2)
        col_p1.info(f"📌 **Cívico-Militar (Faixa Interquartil 50% central):** de **{p25_cm:.2f}** a **{p75_cm:.2f}**")
        col_p2.info(f"📌 **{bench_label} (Faixa Interquartil 50% central):** de **{p25_bench:.2f}** a **{p75_bench:.2f}**")

    with tab_faixas:
        st.subheader("Concentração e Proporção por Faixas de Desempenho")
        
        if metric_col == "TAXA_APROVACAO":
            st.markdown(
                """
                A análise das faixas de aprovação revela o grau de aprovação em massa. 
                Em muitas escolas estaduais do PR, a taxa de aprovação aproxima-se ou atinge exatamente **100%**.
                """
            )
            fig_brackets = make_approval_brackets_bar(df_comp, group_col="GRUPO_COMPARA", title="Distribuição Percentual por Faixa de Aprovação")
            if fig_brackets:
                st.plotly_chart(fig_brackets, use_container_width=True)
                
            # Tabela de faixas de aprovação
            bins = [-np.inf, 85.0, 90.0, 95.0, 98.0, 99.99, 100.01]
            labels = ["< 85%", "85% a 90%", "90% a 95%", "95% a 98%", "98% a 99.9%", "100% (Plena)"]
            df_valid_aprov = df_comp.dropna(subset=["TAXA_APROVACAO", "GRUPO_COMPARA"]).copy()
            df_valid_aprov["FAIXA"] = pd.cut(df_valid_aprov["TAXA_APROVACAO"], bins=bins, labels=labels, right=False)
            
            tabela_faixas = pd.crosstab(df_valid_aprov["FAIXA"], df_valid_aprov["GRUPO_COMPARA"], normalize="columns") * 100
            tabela_faixas_count = pd.crosstab(df_valid_aprov["FAIXA"], df_valid_aprov["GRUPO_COMPARA"])
            
            st.markdown("##### Percentual de Escolas em Cada Faixa de Aprovação (%)")
            st.dataframe(tabela_faixas.style.format("{:.1f}%"), use_container_width=True)
            
        elif "SAEB" in metric_col:
            st.markdown(
                "Abaixo, as escolas são agrupadas por faixas de proficiência ou nota padronizada."
            )
            val_min = df_valid[metric_col].min()
            val_max = df_valid[metric_col].max()
            step = (val_max - val_min) / 4 if (val_max - val_min) > 0 else 1
            bins = [val_min - 0.1, val_min + step, val_min + 2*step, val_min + 3*step, val_max + 0.1]
            labels = ["Nível 1 (Baixo)", "Nível 2 (Básico)", "Nível 3 (Intermediário)", "Nível 4 (Avançado)"]
            df_v = df_valid.copy()
            df_v["FAIXA_SAEB"] = pd.cut(df_v[metric_col], bins=bins, labels=labels)
            tab_saeb = pd.crosstab(df_v["FAIXA_SAEB"], df_v["GRUPO_COMPARA"], normalize="columns") * 100
            st.dataframe(tab_saeb.style.format("{:.1f}%"), use_container_width=True)
            
        else:
            st.info(f"Visualização de faixas para {metric_label}:")
            df_v = df_valid.copy()
            df_v["FAIXA_METRICA"] = pd.qcut(df_v[metric_col], q=4, labels=["Quartil 1", "Quartil 2", "Quartil 3", "Quartil 4"], duplicates="drop")
            tab_q = pd.crosstab(df_v["FAIXA_METRICA"], df_v["GRUPO_COMPARA"], normalize="columns") * 100
            st.dataframe(tab_q.style.format("{:.1f}%"), use_container_width=True)

    with tab_cruzamento:
        st.subheader("Relação entre Taxa de Aprovação e Desempenho no SAEB")
        st.markdown(
            """
            Um aspecto analítico central é verificar se escolas com aprovações muito elevadas 
            apresentam proficiência proporcional nas provas do SAEB, ou se há descolamento entre aprovação formal e aprendizado.
            """
        )
        
        saeb_cross = "SAEB_NOTA_MEDIA" if "SAEB_NOTA_MEDIA" in df_comp.columns else "SAEB_PORTUGUES"
        saeb_cross_label = "Nota Média Padronizada (0 a 10)" if saeb_cross == "SAEB_NOTA_MEDIA" else "Proficiência SAEB"
        
        fig_cross = make_scatter_aprovacao_vs_saeb(
            df_comp,
            saeb_col=saeb_cross,
            saeb_label=saeb_cross_label,
            group_col="GRUPO_COMPARA",
            title=f"Dispersão: Taxa de Aprovação vs {saeb_cross_label}"
        )
        if fig_cross:
            st.plotly_chart(fig_cross, use_container_width=True)
        else:
            st.info("Sem dados suficientes para o cruzamento de aprovação e SAEB.")
            
        st.markdown(
            """
            > [!TIP]
            > **Como interpretar os quadrantes:**
            > - **Superior Direito:** Escolas com alta aprovação e alto desempenho no SAEB (aprendizado com fluxo contínuo).
            > - **Inferior Direito:** Escolas com alta aprovação (> 95%), porém desempenho no SAEB abaixo da média (alerta de aprovação sem proficiência correspondente).
            > - **Superior Esquerdo:** Escolas com nota alta no SAEB, porém taxa de aprovação mais rigorosa/baixa.
            > - **Inferior Esquerdo:** Escolas em situação de vulnerabilidade pedagógica conjunta (baixa aprovação e baixo SAEB).
            """
        )

    with tab_series:
        st.subheader("Taxa de Aprovação por Série / Ano Escolar")
        st.markdown(
            """
            Compara a taxa média de aprovação nos 4 anos/séries da etapa avaliada.
            Permite diagnosticar em qual série ocorre maior retenção ou aprovação.
            """
        )
        
        fig_grades = make_grade_approval_bars(
            df_comp,
            group_col="GRUPO_COMPARA",
            title="Comparativo da Taxa de Aprovação Média por Série/Ano Escolar"
        )
        if fig_grades:
            st.plotly_chart(fig_grades, use_container_width=True)
            
            # Tabela de médias por série
            grade_cols = [c for c in ["TAXA_APROVACAO_1", "TAXA_APROVACAO_2", "TAXA_APROVACAO_3", "TAXA_APROVACAO_4"] if c in df_comp.columns]
            if grade_cols:
                tab_g = df_comp.groupby("GRUPO_COMPARA")[grade_cols].mean().reset_index()
                etapa_pred = df_comp["ETAPA"].mode()[0] if "ETAPA" in df_comp.columns and not df_comp["ETAPA"].empty else ""
                
                if "Médio" in str(etapa_pred):
                    col_names = {"TAXA_APROVACAO_1": "1ª Série", "TAXA_APROVACAO_2": "2ª Série", "TAXA_APROVACAO_3": "3ª Série", "TAXA_APROVACAO_4": "4ª Série"}
                else:
                    col_names = {"TAXA_APROVACAO_1": "6º Ano (1º ciclo)", "TAXA_APROVACAO_2": "7º Ano (2º ciclo)", "TAXA_APROVACAO_3": "8º Ano (3º ciclo)", "TAXA_APROVACAO_4": "9º Ano (4º ciclo)"}
                
                tab_g = tab_g.rename(columns=col_names)
                st.markdown("##### Tabela Detalhada das Médias por Série (%)")
                st.dataframe(
                    tab_g.set_index("GRUPO_COMPARA").style.format("{:.2f}%"),
                    use_container_width=True
                )
        else:
            st.info("Dados de aprovação por série não disponíveis para o recorte atual.")

    with tab_stats:
        st.subheader(f"Sumário Estatístico Completo & Rankings — {metric_label}")
        render_stats_table(df_comp, metric_col, metric_label, group_col="GRUPO_COMPARA")
        
        # Rankings de escolas Cívico-Militares no target selecionado
        df_cm_only = df_comp[df_comp["GRUPO_COMPARA"] == "Cívico-Militar"].dropna(subset=[metric_col])
        if not df_cm_only.empty:
            c_top, c_bot = st.columns(2)
            cols_show = ["NO_ESCOLA", "NO_MUNICIPIO"]
            for col_cand in [metric_col, "SAEB_NOTA_MEDIA", "TAXA_APROVACAO"]:
                if col_cand in df_cm_only.columns and col_cand not in cols_show:
                    cols_show.append(col_cand)

            fmt_dict = {
                metric_col: format_str,
                "SAEB_NOTA_MEDIA": "{:.2f}",
                "TAXA_APROVACAO": "{:.1f}%",
                "TAXA_NAO_APROVACAO": "{:.1f}%",
                "IDEB_OBSERVADO": "{:.2f}",
                "SAEB_PORTUGUES": "{:.2f}",
                "SAEB_MATEMATICA": "{:.2f}",
            }
            fmt_show = {c: fmt_dict[c] for c in cols_show if c in fmt_dict}
            
            with c_top:
                st.markdown(f"##### 🔼 Top 10 Escolas Cívico-Militares ({metric_label})")
                top10 = df_cm_only.sort_values(metric_col, ascending=False).head(10)[cols_show]
                st.dataframe(
                    top10.style.format(fmt_show, na_rep="-"),
                    use_container_width=True,
                    hide_index=True
                )
                
            with c_bot:
                st.markdown(f"##### 🔽 10 Menores Índices entre Cívico-Militares ({metric_label})")
                bot10 = df_cm_only.sort_values(metric_col, ascending=True).head(10)[cols_show]
                st.dataframe(
                    bot10.style.format(fmt_show, na_rep="-"),
                    use_container_width=True,
                    hide_index=True
                )
