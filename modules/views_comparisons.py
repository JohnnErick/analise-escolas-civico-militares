import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from modules.components import render_kpi_cards, render_stats_table
from modules.data_loader import load_comparisons_dataset
from modules.charts import (
    COLOR_MAP,
    make_boxplot_comparison,
    make_histogram_comparison,
    make_scatter_aprovacao_vs_saeb,
    make_grade_approval_bars,
    make_approval_brackets_bar
)

def render_comparisons_view(df: pd.DataFrame = None, df_raw: pd.DataFrame = None):
    """
    Renderiza a Central de Comparações e Benchmarks entre escolas Cívico-Militares e Não Cívico-Militares.
    Permite comparar aprovação, reprovação, abandono, proficiências SAEB e notas IDEB.
    """
    st.header("⚖️ Central de Comparações & Benchmarks Educacionais")
    st.markdown(
        """
        Esta seção compara o desempenho e indicadores de fluxo dos colégios **Cívico-Militares** 
        contra diferentes **grupos de referência (benchmarks)** da rede escolar paranaense, 
        abrangendo aprovação, reprovação, abandono, proficiências do SAEB e IDEB.
        """
    )
    
    # Carregamento de dados unificados com cache se não fornecidos
    if df_raw is None or df_raw.empty:
        try:
            df_raw = load_comparisons_dataset()
        except Exception as e:
            st.error(f"Erro ao carregar a base unificada de dados: {e}")
            return
            
    if df_raw.empty:
        st.warning("A base de dados comparativa não contém registros disponíveis.")
        return

    # ==========================================
    # PAINEL DE FILTROS CONTEXTUAIS
    # ==========================================
    with st.expander("🎛️ Filtros de Recorte e Amostra", expanded=True):
        f1, f2, f3, f4 = st.columns([1.5, 2.0, 2.0, 2.5])
        with f1:
            anos_disp = sorted([int(a) for a in df_raw["ANO"].dropna().unique() if a in [2023, 2021, 2019, 2017, 2015, 2013, 2011, 2009, 2007, 2005]], reverse=True)
            ano_selecionado = st.selectbox(
                "Ano de Referência:",
                options=anos_disp,
                index=0,  # Padrão: 2023 (ciclo mais recente com Censo e SAEB completos)
                help="Selecione a edição censitária ou ciclo do SAEB/IDEB.",
                key="comp_filter_ano"
            )
        with f2:
            etapas_disp = ["Anos Finais (6º-9º)", "Ensino Médio", "Todas as Etapas", "Anos Iniciais (1º-5º)"]
            etapa_selecionada = st.selectbox(
                "Etapa de Ensino:",
                options=etapas_disp,
                index=0,  # Padrão: Anos Finais (etapa central de implantação do programa)
                help="O programa cívico-militar concentra-se prioritariamente nos Anos Finais.",
                key="comp_filter_etapa"
            )
        with f3:
            redes_disp = ["Rede Estadual (SEED-PR)", "Todas as Redes (Estadual, Municipal, Privada)"]
            rede_selecionada = st.selectbox(
                "Rede de Ensino:",
                options=redes_disp,
                index=0,  # Padrão: Estadual (comparação justa e simétrica)
                help="A Rede Estadual é o parâmetro mais simétrico para avaliar colégios estaduais.",
                key="comp_filter_rede"
            )
        with f4:
            criterio_ccm = st.selectbox(
                "Critério de Enquadramento CCM:",
                options=[
                    "Universo Oficial SEED-PR (306 colégios)",
                    "Universo Auditado dos Editais 2024 (106 colégios ativos)",
                    "Grupo Quase-Experimental (62 escolas com consulta não convertida)"
                ],
                index=0,
                help=(
                    "• Universo Oficial SEED-PR: Relação ampla dos colégios da rede estadual participantes do programa.\n"
                    "• Universo Auditado 2024: Apenas unidades com homologação formal publicada em Diário Oficial para 2024.\n"
                    "• Grupo Quase-Experimental: Escolas selecionadas para consulta que mantiveram o modelo regular civil (contrafactual)."
                ),
                key="comp_filter_criterio"
            )
            
        col_mun, col_busca = st.columns([3, 3])
        with col_mun:
            muns_disp = ["Todos os Municípios"] + sorted(df_raw["NO_MUNICIPIO"].dropna().unique().tolist())
            mun_selecionado = st.selectbox(
                "Filtrar por Município (Opcional):",
                options=muns_disp,
                index=0,
                key="comp_filter_mun"
            )
        with col_busca:
            busca_textual = st.text_input(
                "Buscar escola na comparação:",
                placeholder="Ex: Alberto Krause, 41122801...",
                key="comp_filter_busca"
            ).strip().lower()

    # Aplica os filtros na base de trabalho
    df_work = df_raw.copy()
    if ano_selecionado:
        df_work = df_work[df_work["ANO"] == ano_selecionado]
    if etapa_selecionada != "Todas as Etapas":
        df_work = df_work[df_work["ETAPA"] == etapa_selecionada]
    if rede_selecionada == "Rede Estadual (SEED-PR)":
        df_work = df_work[df_work["REDE"] == "Estadual"]
    if mun_selecionado != "Todos os Municípios":
        df_work = df_work[df_work["NO_MUNICIPIO"] == mun_selecionado]
    if busca_textual:
        cond_n = df_work["NO_ESCOLA"].astype(str).str.lower().str.contains(busca_textual, na=False)
        cond_i = df_work["ID_ESCOLA"].astype(str).str.contains(busca_textual, na=False)
        df_work = df_work[cond_n | cond_i]

    # Ajusta a rotulagem de TIPO_GESTAO de acordo com o critério escolhido
    if criterio_ccm == "Universo Auditado dos Editais 2024 (106 colégios ativos)":
        if "status_ccm_atual" in df_work.columns:
            df_work["TIPO_GESTAO"] = np.where(df_work["status_ccm_atual"] == "SIM", "Cívico-Militar", "Não Cívico-Militar")
    elif criterio_ccm == "Grupo Quase-Experimental (62 escolas com consulta não convertida)":
        if "status_ccm_atual" in df_work.columns:
            # Compara as 106 ativas com as 62 consultadas não convertidas
            is_cm = df_work["status_ccm_atual"] == "SIM"
            is_ind = df_work["status_ccm_atual"] == "INDETERMINADO"
            df_work = df_work[is_cm | is_ind].copy()
            df_work["TIPO_GESTAO"] = np.where(df_work["status_ccm_atual"] == "SIM", "Cívico-Militar", "Não Cívico-Militar")

    # ==========================================
    # BARRA DE SELEÇÃO: TARGET & BENCHMARK
    # ==========================================
    st.markdown("#### 🎯 Configuração do Target de Comparação")
    col_target, col_bench, col_filtro_extra = st.columns([2.5, 2.3, 1.2])
    
    TARGET_OPTIONS = [
        (
            "TAXA_APROVACAO",
            "📋 Taxa de Aprovação Escolar (%)",
            "{:.1f}%",
            "Taxa de Aprovação (%)",
            "Percentual de estudantes aprovados no ano letivo. O debate educacional destaca a frequência de taxas de aprovação próximas a 100% e sua relação com a proficiência real."
        ),
        (
            "TAXA_NAO_APROVACAO",
            "⚠️ Taxa de Não-Aprovação (Reprovação + Abandono %)",
            "{:.1f}%",
            "Não-Aprovação (%)",
            "Percentual de retenção ou evasão (100% - Taxa de Aprovação). Sintetiza o fluxo de interrupção ou atraso na trajetória escolar."
        ),
        (
            "TAXA_REPROVACAO",
            "🛑 Taxa de Reprovação (%)",
            "{:.1f}%",
            "Taxa de Reprovação (%)",
            "Percentual de estudantes retidos na série escolar ao término do ano letivo (Fonte: Censo Escolar/INEP)."
        ),
        (
            "TAXA_ABANDONO",
            "🏃 Taxa de Abandono / Evasão (%)",
            "{:.1f}%",
            "Taxa de Abandono (%)",
            "Percentual de estudantes que deixaram de frequentar a escola no decorrer do ano letivo (Fonte: Censo Escolar/INEP)."
        ),
        (
            "SAEB_NOTA_MEDIA",
            "⭐ SAEB — Nota Média Padronizada (0 a 10)",
            "{:.2f}",
            "Nota Média SAEB (0-10)",
            "Nota padronizada calculada pelo INEP a partir do rendimento de Língua Portuguesa e Matemática (fator N do IDEB)."
        ),
        (
            "SAEB_PORTUGUES",
            "📖 SAEB — Língua Portuguesa (Pontos)",
            "{:.1f}",
            "Proficiência Língua Portuguesa",
            "Escala de proficiência do SAEB para domínio de leitura e compreensão de texto."
        ),
        (
            "SAEB_MATEMATICA",
            "📐 SAEB — Matemática (Pontos)",
            "{:.1f}",
            "Proficiência Matemática",
            "Escala de proficiência do SAEB para raciocínio lógico e resolução de problemas matemáticos."
        ),
        (
            "IDEB_OBSERVADO",
            "🏆 IDEB Observado (0 a 10)",
            "{:.2f}",
            "IDEB Observado",
            "Índice de Desenvolvimento da Educação Básica: sintetiza aprendizagem padronizada (SAEB) e taxa de aprovação (IDEB = N × P)."
        ),
        (
            "INDICADOR_RENDIMENTO",
            "📈 Indicador de Rendimento (0 a 1)",
            "{:.3f}",
            "Indicador de Rendimento (P)",
            "Média harmônica das taxas de aprovação nas séries da etapa avaliada (fator P da fórmula do IDEB)."
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
            "Selecione o Indicador-Alvo (Target):",
            options=range(len(TARGET_OPTIONS)),
            format_func=lambda i: TARGET_OPTIONS[i][1],
            index=0,  # Padrão: Taxa de Aprovação
            help="Escolha qual indicador educacional estará no foco da análise comparativa.",
            key="comp_target_idx"
        )
        
    metric_col, metric_label, format_str, y_axis_label, metric_desc = TARGET_OPTIONS[idx_target]
    
    with col_bench:
        benchmark_choice = st.selectbox(
            "Grupo de Comparação (Benchmark):",
            options=[
                "Rede Estadual Regular (Não CM)",
                "Não Cívico-Militar (Geral)",
                "Mesmo Município (Pareamento Territorial)"
            ],
            index=0,  # Padrão: Rede Estadual Regular
            help=(
                "• Rede Estadual Regular: Compara apenas com colégios estaduais tradicionais (exclui redes municipais/privadas).\n"
                "• Mesmo Município: Restringe a comparação às escolas regulares situadas nos mesmos municípios onde há colégios cívico-militares."
            ),
            key="comp_bench_sel"
        )
        
    with col_filtro_extra:
        filtro_amostra = st.selectbox(
            "Amostra:",
            options=["Todas", "Com SAEB"],
            index=0,
            key="comp_amostra_sel"
        )
        
    st.caption(f"ℹ️ **Sobre este target:** {metric_desc}")
    
    # ==========================================
    # CONSTRUÇÃO DO GRUPO COMPARATIVO
    # ==========================================
    # Assegura existência da métrica
    if metric_col not in df_work.columns:
        df_work[metric_col] = np.nan
        
    df_work[metric_col] = pd.to_numeric(df_work[metric_col], errors="coerce")
    
    if filtro_amostra == "Com SAEB" and "SAEB_PORTUGUES" in df_work.columns:
        df_work = df_work[df_work["SAEB_PORTUGUES"].notna() & df_work["SAEB_MATEMATICA"].notna()]
        
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
        cm_part = df_work[df_work["TIPO_GESTAO"] == "Cívico-Militar"].copy()
        cm_part["GRUPO_COMPARA"] = "Cívico-Militar"
        ncm_part = df_work[df_work["TIPO_GESTAO"] == "Não Cívico-Militar"].copy()
        ncm_part["GRUPO_COMPARA"] = "Não Cívico-Militar"
        df_comp = pd.concat([cm_part, ncm_part], ignore_index=True)
        bench_label = "Não Cívico-Militar"
        
    df_valid = df_comp.dropna(subset=[metric_col, "GRUPO_COMPARA"])
    
    if df_valid.empty:
        st.warning(
            f"Não há observações com o indicador '{metric_label}' preenchido "
            f"para o ano {ano_selecionado} e etapa '{etapa_selecionada}' com os filtros atuais."
        )
        return
        
    st.markdown("---")
    
    # ==========================================
    # CARTÕES KPI COMPARATIVOS
    # ==========================================
    st.markdown(f"##### 📊 Indicadores Comparativos: **{metric_label}** ({ano_selecionado})")
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
        "📋 Sumário Estatístico & Rankings"
    ])
    
    with tab_dist:
        st.subheader(f"Distribuição Estatística — {metric_label}")
        st.markdown(
            f"Comparação da dispersão dos dados entre **Cívico-Militar** e **{bench_label}**."
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
        cm_vals = df_comp[df_comp["GRUPO_COMPARA"] == "Cívico-Militar"][metric_col].dropna()
        bench_vals = df_comp[df_comp["GRUPO_COMPARA"] == bench_label][metric_col].dropna()
        
        if not cm_vals.empty and not bench_vals.empty:
            col_p1, col_p2 = st.columns(2)
            col_p1.info(f"📌 **Cívico-Militar (50% central / Q1 a Q3):** de **{cm_vals.quantile(0.25):.2f}** a **{cm_vals.quantile(0.75):.2f}**")
            col_p2.info(f"📌 **{bench_label} (50% central / Q1 a Q3):** de **{bench_vals.quantile(0.25):.2f}** a **{bench_vals.quantile(0.75):.2f}**")

    with tab_faixas:
        st.subheader("Concentração e Proporção por Faixas de Desempenho")
        
        if metric_col == "TAXA_APROVACAO":
            st.markdown(
                """
                A análise das faixas de aprovação evidencia a concentração de escolas com aprovação máxima. 
                Em diversas escolas do Paraná, a taxa de aprovação atinge exatamente **100%**.
                """
            )
            fig_brackets = make_approval_brackets_bar(
                df_comp,
                group_col="GRUPO_COMPARA",
                title="Distribuição Percentual por Faixa de Aprovação"
            )
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
            
        elif metric_col in ["TAXA_REPROVACAO", "TAXA_ABANDONO"]:
            st.markdown(f"Distribuição de escolas por faixas de **{metric_label}**:")
            bins = [-np.inf, 0.01, 2.0, 5.0, 10.0, np.inf]
            labels = ["Zero (0%)", "Até 2.0%", "2.0% a 5.0%", "5.0% a 10.0%", "Acima de 10.0%"]
            df_v = df_valid.copy()
            df_v["FAIXA_FLUXO"] = pd.cut(df_v[metric_col], bins=bins, labels=labels, right=False)
            tab_fluxo = pd.crosstab(df_v["FAIXA_FLUXO"], df_v["GRUPO_COMPARA"], normalize="columns") * 100
            st.dataframe(tab_fluxo.style.format("{:.1f}%"), use_container_width=True)
            
        elif "SAEB" in metric_col:
            st.markdown(f"Agrupamento de escolas por quartis ou níveis de proficiência em **{metric_label}**:")
            val_min = df_valid[metric_col].min()
            val_max = df_valid[metric_col].max()
            step = (val_max - val_min) / 4 if (val_max - val_min) > 0 else 1
            bins = [val_min - 0.1, val_min + step, val_min + 2*step, val_min + 3*step, val_max + 0.1]
            labels = ["Nível 1 (Básico Inicial)", "Nível 2 (Básico)", "Nível 3 (Adequado)", "Nível 4 (Avançado)"]
            df_v = df_valid.copy()
            df_v["FAIXA_SAEB"] = pd.cut(df_v[metric_col], bins=bins, labels=labels)
            tab_saeb = pd.crosstab(df_v["FAIXA_SAEB"], df_v["GRUPO_COMPARA"], normalize="columns") * 100
            st.dataframe(tab_saeb.style.format("{:.1f}%"), use_container_width=True)
            
        else:
            st.info(f"Visualização de faixas para {metric_label}:")
            df_v = df_valid.copy()
            df_v["FAIXA_METRICA"] = pd.qcut(df_v[metric_col], q=4, labels=["Quartil 1 (Menores)", "Quartil 2", "Quartil 3", "Quartil 4 (Maiores)"], duplicates="drop")
            tab_q = pd.crosstab(df_v["FAIXA_METRICA"], df_v["GRUPO_COMPARA"], normalize="columns") * 100
            st.dataframe(tab_q.style.format("{:.1f}%"), use_container_width=True)

    with tab_cruzamento:
        st.subheader("Relação entre Taxa de Aprovação e Desempenho no SAEB")
        st.markdown(
            """
            Um teste pedagógico central consiste em examinar se taxas de aprovação elevadas 
            são acompanhadas de proficiência correspondente nas avaliações censitárias do SAEB, 
            ou se existe descolamento entre aprovação formal e aprendizado efetivo.
            """
        )
        
        saeb_cross = "SAEB_NOTA_MEDIA" if "SAEB_NOTA_MEDIA" in df_comp.columns and df_comp["SAEB_NOTA_MEDIA"].notna().sum() > 0 else "SAEB_PORTUGUES"
        saeb_cross_label = "Nota Média Padronizada (0 a 10)" if saeb_cross == "SAEB_NOTA_MEDIA" else "Proficiência Língua Portuguesa"
        
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
            st.info("Sem dados suficientes para o cruzamento entre aprovação e SAEB no recorte selecionado.")
            
        st.markdown(
            """
            > [!TIP]
            > **Interpretação dos quadrantes:**
            > - **Superior Direito:** Escolas com alta aprovação e alta nota no SAEB (fluxo contínuo com aprendizado comprovado).
            > - **Inferior Direito:** Escolas com alta taxa de aprovação (> 95%), porém nota SAEB abaixo da média (alerta de aprovação formal com defasagem de aprendizagem).
            > - **Superior Esquerdo:** Escolas com proficiência elevada no SAEB, com critérios de retenção mais rigorosos.
            > - **Inferior Esquerdo:** Escolas em situação de vulnerabilidade pedagógica conjunta (baixa aprovação e baixo desempenho SAEB).
            """
        )

    with tab_series:
        st.subheader("Taxa de Aprovação por Série / Ano Escolar")
        st.markdown(
            """
            Desagrega a taxa média de aprovação nos 4 anos/séries da etapa selecionada, 
            permitindo identificar em qual série do ciclo ocorre maior retenção ou aprovação.
            """
        )
        
        fig_grades = make_grade_approval_bars(
            df_comp,
            group_col="GRUPO_COMPARA",
            title="Comparativo da Taxa de Aprovação Média por Série/Ano Escolar"
        )
        if fig_grades:
            st.plotly_chart(fig_grades, use_container_width=True)
            
            # Tabela discriminada por série
            grade_cols = [c for c in ["TAXA_APROVACAO_1", "TAXA_APROVACAO_2", "TAXA_APROVACAO_3", "TAXA_APROVACAO_4"] if c in df_comp.columns]
            if grade_cols:
                tab_g = df_comp.groupby("GRUPO_COMPARA")[grade_cols].mean().reset_index()
                etapa_pred = df_comp["ETAPA"].mode()[0] if "ETAPA" in df_comp.columns and not df_comp["ETAPA"].empty else ""
                
                if "Médio" in str(etapa_pred):
                    col_names = {"TAXA_APROVACAO_1": "1ª Série", "TAXA_APROVACAO_2": "2ª Série", "TAXA_APROVACAO_3": "3ª Série", "TAXA_APROVACAO_4": "4ª Série"}
                elif "Iniciais" in str(etapa_pred):
                    col_names = {"TAXA_APROVACAO_1": "1º/2º Ano", "TAXA_APROVACAO_2": "3º Ano", "TAXA_APROVACAO_3": "4º Ano", "TAXA_APROVACAO_4": "5º Ano"}
                else:
                    col_names = {"TAXA_APROVACAO_1": "6º Ano", "TAXA_APROVACAO_2": "7º Ano", "TAXA_APROVACAO_3": "8º Ano", "TAXA_APROVACAO_4": "9º Ano"}
                
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
            for col_cand in [metric_col, "TAXA_APROVACAO", "SAEB_NOTA_MEDIA", "IDEB_OBSERVADO"]:
                if col_cand in df_cm_only.columns and col_cand not in cols_show:
                    cols_show.append(col_cand)

            fmt_dict = {
                metric_col: format_str,
                "TAXA_APROVACAO": "{:.1f}%",
                "TAXA_NAO_APROVACAO": "{:.1f}%",
                "TAXA_REPROVACAO": "{:.1f}%",
                "TAXA_ABANDONO": "{:.1f}%",
                "SAEB_NOTA_MEDIA": "{:.2f}",
                "IDEB_OBSERVADO": "{:.2f}",
                "SAEB_PORTUGUES": "{:.1f}",
                "SAEB_MATEMATICA": "{:.1f}",
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

        # Botão de exportação do recorte
        st.markdown("---")
        col_exp1, _ = st.columns([2, 4])
        with col_exp1:
            csv_data = df_comp.to_csv(index=False, sep=";", decimal=",", encoding="utf-8-sig")
            st.download_button(
                label="📥 Baixar Dados Deste Recorte (CSV)",
                data=csv_data,
                file_name=f"comparativo_{metric_col.lower()}_{ano_selecionado}.csv",
                mime="text/csv",
                use_container_width=True
            )
