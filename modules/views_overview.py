import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from modules.data_loader import load_cadastro, load_historico_ano, load_comparisons_dataset
from modules.charts import COLOR_MAP, CHART_THEME

def render_overview_comparison_section(df_raw: pd.DataFrame = None):
    """
    Renderiza seção comparativa executiva entre escolas no modelo Cívico-Militar e fora do modelo (Rede Regular).
    Abrange Taxa de Aprovação, Notas SAEB (Língua Portuguesa e Matemática) e IDEB.
    """
    st.markdown("### ⚖️ Comparação Educacional: Modelo Cívico-Militar vs. Fora do Modelo (Rede Regular)")
    st.markdown(
        """
        Comparativo descritivo agregado entre os estabelecimentos de ensino no modelo **Cívico-Militar (CCM)** 
        e as escolas da **Rede Regular Estadual (fora do modelo)**, cobrindo indicadores oficiais de fluxo 
        (Taxa de Aprovação) e proficiência/desempenho escolar (SAEB Língua Portuguesa, SAEB Matemática e IDEB).
        """
    )
    
    if df_raw is None or df_raw.empty:
        try:
            df_raw = load_comparisons_dataset()
        except Exception as e:
            st.warning(f"Não foi possível carregar a base comparativa no momento: {e}")
            return
            
    if df_raw.empty:
        st.warning("Base comparativa sem registros disponíveis.")
        return

    # Controles compactos de recorte
    c_ano, c_etapa, c_info = st.columns([1.5, 2.0, 3.5])
    with c_ano:
        anos_disp = sorted([int(a) for a in df_raw["ANO"].dropna().unique() if a in [2023, 2021, 2019, 2017]], reverse=True)
        sel_ano = st.selectbox(
            "Ano de Referência:",
            options=anos_disp,
            index=0 if 2023 in anos_disp else 0,
            key="overview_comp_ano",
            help="Último ciclo oficial consolidado com dados de aprovação do Censo Escolar e avaliações do SAEB/IDEB."
        )
    with c_etapa:
        etapas_disp = ["Anos Finais (6º-9º)", "Ensino Médio"]
        sel_etapa = st.selectbox(
            "Etapa de Ensino:",
            options=etapas_disp,
            index=0,
            key="overview_comp_etapa",
            help="O programa CCM concentra-se majoritariamente nos Anos Finais do Ensino Fundamental."
        )

    # Filtrar na Rede Estadual para manter simetria metodológica
    sub = df_raw[(df_raw["ANO"] == sel_ano) & (df_raw["REDE"] == "Estadual") & (df_raw["ETAPA"] == sel_etapa)].copy()
    
    ccm_sub = sub[sub["TIPO_GESTAO"] == "Cívico-Militar"]
    reg_sub = sub[sub["TIPO_GESTAO"] == "Não Cívico-Militar"]
    
    n_ccm = len(ccm_sub)
    n_reg = len(reg_sub)
    
    with c_info:
        st.write("")
        st.caption(
            f"🎯 **Escopo Auditado:** Rede Estadual do Paraná &bull; "
            f"**{n_ccm:,}** escolas CCM e **{n_reg:,}** escolas Regulares na base de **{sel_ano}**."
        )
        
    if n_ccm == 0 or n_reg == 0:
        st.warning(f"Não há registros suficientes para o cruzamento selecionado ({sel_ano} — {sel_etapa}).")
        return

    # Cálculos das métricas
    # 1. Aprovação
    aprov_ccm = ccm_sub["TAXA_APROVACAO"].dropna()
    aprov_reg = reg_sub["TAXA_APROVACAO"].dropna()
    m_aprov_ccm = aprov_ccm.mean() if len(aprov_ccm) else None
    m_aprov_reg = aprov_reg.mean() if len(aprov_reg) else None
    delta_aprov = (m_aprov_ccm - m_aprov_reg) if (m_aprov_ccm is not None and m_aprov_reg is not None) else None
    
    # 2. SAEB Língua Portuguesa
    lp_ccm = ccm_sub["SAEB_PORTUGUES"].dropna()
    lp_reg = reg_sub["SAEB_PORTUGUES"].dropna()
    m_lp_ccm = lp_ccm.mean() if len(lp_ccm) else None
    m_lp_reg = lp_reg.mean() if len(lp_reg) else None
    delta_lp = (m_lp_ccm - m_lp_reg) if (m_lp_ccm is not None and m_lp_reg is not None) else None
    
    # 3. SAEB Matemática
    mt_ccm = ccm_sub["SAEB_MATEMATICA"].dropna()
    mt_reg = reg_sub["SAEB_MATEMATICA"].dropna()
    m_mt_ccm = mt_ccm.mean() if len(mt_ccm) else None
    m_mt_reg = mt_reg.mean() if len(mt_reg) else None
    delta_mt = (m_mt_ccm - m_mt_reg) if (m_mt_ccm is not None and m_mt_reg is not None) else None
    
    # 4. IDEB Observado
    ideb_ccm = ccm_sub["IDEB_OBSERVADO"].dropna()
    ideb_reg = reg_sub["IDEB_OBSERVADO"].dropna()
    m_ideb_ccm = ideb_ccm.mean() if len(ideb_ccm) else None
    m_ideb_reg = ideb_reg.mean() if len(ideb_reg) else None
    delta_ideb = (m_ideb_ccm - m_ideb_reg) if (m_ideb_ccm is not None and m_ideb_reg is not None) else None

    # Cartões de KPIs Comparativos
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric(
            label="📋 Taxa de Aprovação",
            value=f"{m_aprov_ccm:.1f}%" if m_aprov_ccm is not None else "N/D",
            delta=f"{delta_aprov:+.1f} p.p. vs Regular" if delta_aprov is not None else None,
            help=f"Média CCM: {m_aprov_ccm:.1f}% (N={len(aprov_ccm)}) | Média Regular: {m_aprov_reg:.1f}% (N={len(aprov_reg)})"
        )
        st.caption(f"Regular: **{m_aprov_reg:.1f}%**" if m_aprov_reg is not None else "")
        
    with k2:
        st.metric(
            label="📖 SAEB — Português",
            value=f"{m_lp_ccm:.1f}" if m_lp_ccm is not None else "N/D",
            delta=f"{delta_lp:+.1f} pts vs Regular" if delta_lp is not None else None,
            help=f"Média CCM: {m_lp_ccm:.1f} pts (N={len(lp_ccm)}) | Média Regular: {m_lp_reg:.1f} pts (N={len(lp_reg)})"
        )
        st.caption(f"Regular: **{m_lp_reg:.1f} pts**" if m_lp_reg is not None else "")
        
    with k3:
        st.metric(
            label="📐 SAEB — Matemática",
            value=f"{m_mt_ccm:.1f}" if m_mt_ccm is not None else "N/D",
            delta=f"{delta_mt:+.1f} pts vs Regular" if delta_mt is not None else None,
            help=f"Média CCM: {m_mt_ccm:.1f} pts (N={len(mt_ccm)}) | Média Regular: {m_mt_reg:.1f} pts (N={len(mt_reg)})"
        )
        st.caption(f"Regular: **{m_mt_reg:.1f} pts**" if m_mt_reg is not None else "")
        
    with k4:
        st.metric(
            label="🏆 IDEB Observado",
            value=f"{m_ideb_ccm:.2f}" if m_ideb_ccm is not None else "N/D",
            delta=f"{delta_ideb:+.2f} vs Regular" if delta_ideb is not None else None,
            help=f"Média CCM: {m_ideb_ccm:.2f} (N={len(ideb_ccm)}) | Média Regular: {m_ideb_reg:.2f} (N={len(ideb_reg)})"
        )
        st.caption(f"Regular: **{m_ideb_reg:.2f}**" if m_ideb_reg is not None else "")

    st.write("")
    
    # Abas com visualizações gráficas e tabela
    tab_graf, tab_disp, tab_tab = st.tabs([
        "📊 Médias Comparativas", 
        "📦 Distribuição & Dispersão (Boxplot)", 
        "📋 Tabela Estruturada & Amostra"
    ])
    
    with tab_graf:
        col_g1, col_g2 = st.columns(2)
        
        # Gráfico A: Proficiências SAEB (Língua Portuguesa e Matemática)
        with col_g1:
            df_bar_saeb = pd.DataFrame([
                {"Disciplina": "Língua Portuguesa", "Grupo": "Cívico-Militar", "Média": m_lp_ccm},
                {"Disciplina": "Língua Portuguesa", "Grupo": "Não Cívico-Militar", "Média": m_lp_reg},
                {"Disciplina": "Matemática", "Grupo": "Cívico-Militar", "Média": m_mt_ccm},
                {"Disciplina": "Matemática", "Grupo": "Não Cívico-Militar", "Média": m_mt_reg},
            ])
            fig_saeb = px.bar(
                df_bar_saeb,
                x="Disciplina",
                y="Média",
                color="Grupo",
                barmode="group",
                color_discrete_map=COLOR_MAP,
                text_auto=".1f",
                title=f"Proficiência SAEB (Pontos) — {sel_ano}",
                labels={"Média": "Proficiência Média (Pontos)", "Disciplina": ""},
                template=CHART_THEME
            )
            fig_saeb.update_traces(textposition="outside", textfont_size=12)
            saeb_vals = [v for v in [m_lp_ccm, m_lp_reg, m_mt_ccm, m_mt_reg] if v is not None]
            min_y = (min(saeb_vals) - 15) if saeb_vals else 200
            max_y = (max(saeb_vals) + 15) if saeb_vals else 300
            fig_saeb.update_layout(
                yaxis=dict(range=[max(0, min_y), max_y]),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=20, r=20, t=50, b=20)
            )
            st.plotly_chart(fig_saeb, use_container_width=True)

        # Gráfico B: Taxa de Aprovação Escolar (%)
        with col_g2:
            df_bar_fluxo = pd.DataFrame([
                {"Métrica": "Aprovação", "Grupo": "Cívico-Militar", "Valor": m_aprov_ccm},
                {"Métrica": "Aprovação", "Grupo": "Não Cívico-Militar", "Valor": m_aprov_reg},
            ])
            fig_fluxo = px.bar(
                df_bar_fluxo,
                x="Métrica",
                y="Valor",
                color="Grupo",
                barmode="group",
                color_discrete_map=COLOR_MAP,
                text_auto=".1f",
                title=f"Taxa de Aprovação Escolar (%) — {sel_ano}",
                labels={"Valor": "Aprovação Média (%)", "Métrica": ""},
                template=CHART_THEME
            )
            fig_fluxo.update_traces(textposition="outside", textfont_size=12)
            fig_fluxo.update_layout(
                yaxis=dict(range=[85, 103]),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=20, r=20, t=50, b=20)
            )
            st.plotly_chart(fig_fluxo, use_container_width=True)

        col_g3, col_g4 = st.columns(2)
        
        # Gráfico C: IDEB Observado
        with col_g3:
            df_bar_ideb = pd.DataFrame([
                {"Métrica": "IDEB", "Grupo": "Cívico-Militar", "Valor": m_ideb_ccm},
                {"Métrica": "IDEB", "Grupo": "Não Cívico-Militar", "Valor": m_ideb_reg},
            ])
            fig_ideb = px.bar(
                df_bar_ideb,
                x="Métrica",
                y="Valor",
                color="Grupo",
                barmode="group",
                color_discrete_map=COLOR_MAP,
                text_auto=".2f",
                title=f"IDEB Observado (0 a 10) — {sel_ano}",
                labels={"Valor": "IDEB Médio", "Métrica": ""},
                template=CHART_THEME
            )
            fig_ideb.update_traces(textposition="outside", textfont_size=12)
            ideb_vals = [v for v in [m_ideb_ccm, m_ideb_reg] if v is not None]
            min_ideb = (min(ideb_vals) - 0.8) if ideb_vals else 3.0
            max_ideb = (max(ideb_vals) + 0.8) if ideb_vals else 7.0
            fig_ideb.update_layout(
                yaxis=dict(range=[max(0.0, min_ideb), max_ideb]),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=20, r=20, t=50, b=20)
            )
            st.plotly_chart(fig_ideb, use_container_width=True)

        # Gráfico D: Variação Relativa (%) CCM vs. Não CCM
        with col_g4:
            pct_lp = (delta_lp / m_lp_reg * 100) if (delta_lp is not None and m_lp_reg) else 0
            pct_mt = (delta_mt / m_mt_reg * 100) if (delta_mt is not None and m_mt_reg) else 0
            pct_aprov = (delta_aprov / m_aprov_reg * 100) if (delta_aprov is not None and m_aprov_reg) else 0
            pct_ideb = (delta_ideb / m_ideb_reg * 100) if (delta_ideb is not None and m_ideb_reg) else 0
            
            df_bar_diff = pd.DataFrame([
                {"Indicador": "SAEB Português", "Diferença Relativa (%)": pct_lp},
                {"Indicador": "SAEB Matemática", "Diferença Relativa (%)": pct_mt},
                {"Indicador": "Aprovação (%)", "Diferença Relativa (%)": pct_aprov},
                {"Indicador": "IDEB Observado", "Diferença Relativa (%)": pct_ideb},
            ])
            df_bar_diff["Sinal"] = np.where(df_bar_diff["Diferença Relativa (%)"] >= 0, "Superior no CCM", "Superior na Regular")
            diff_colors = {"Superior no CCM": "#1E3A8A", "Superior na Regular": "#64748B"}
            fig_diff = px.bar(
                df_bar_diff,
                x="Indicador",
                y="Diferença Relativa (%)",
                color="Sinal",
                color_discrete_map=diff_colors,
                text_auto="+.2f",
                title=f"Diferença Relativa (%) das Médias CCM vs. Regular",
                labels={"Diferença Relativa (%)": "Variação (%)", "Indicador": ""},
                template=CHART_THEME
            )
            fig_diff.update_traces(textposition="outside", textfont_size=12)
            fig_diff.update_layout(
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=20, r=20, t=50, b=20)
            )
            st.plotly_chart(fig_diff, use_container_width=True)

    with tab_disp:
        st.caption(
            "📌 **Análise de Dispersão:** As médias resumem a tendência central, mas cada escola possui sua própria realidade. "
            "Os gráficos abaixo exibem a dispersão e quartis das escolas em cada grupo para demonstrar a sobreposição real entre as redes."
        )
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            fig_box_lp = px.box(
                sub.dropna(subset=["SAEB_PORTUGUES", "TIPO_GESTAO"]),
                x="TIPO_GESTAO",
                y="SAEB_PORTUGUES",
                color="TIPO_GESTAO",
                color_discrete_map=COLOR_MAP,
                points="outliers",
                title="Dispersão: SAEB Língua Portuguesa",
                labels={"TIPO_GESTAO": "Grupo", "SAEB_PORTUGUES": "Proficiência (Pontos)"},
                template=CHART_THEME
            )
            fig_box_lp.update_layout(showlegend=False, margin=dict(l=20, r=20, t=40, b=20), xaxis_title="")
            st.plotly_chart(fig_box_lp, use_container_width=True)
            
        with col_d2:
            fig_box_mt = px.box(
                sub.dropna(subset=["SAEB_MATEMATICA", "TIPO_GESTAO"]),
                x="TIPO_GESTAO",
                y="SAEB_MATEMATICA",
                color="TIPO_GESTAO",
                color_discrete_map=COLOR_MAP,
                points="outliers",
                title="Dispersão: SAEB Matemática",
                labels={"TIPO_GESTAO": "Grupo", "SAEB_MATEMATICA": "Proficiência (Pontos)"},
                template=CHART_THEME
            )
            fig_box_mt.update_layout(showlegend=False, margin=dict(l=20, r=20, t=40, b=20), xaxis_title="")
            st.plotly_chart(fig_box_mt, use_container_width=True)

        col_d3, col_d4 = st.columns(2)
        with col_d3:
            fig_box_aprov = px.box(
                sub.dropna(subset=["TAXA_APROVACAO", "TIPO_GESTAO"]),
                x="TIPO_GESTAO",
                y="TAXA_APROVACAO",
                color="TIPO_GESTAO",
                color_discrete_map=COLOR_MAP,
                points="outliers",
                title="Dispersão: Taxa de Aprovação (%)",
                labels={"TIPO_GESTAO": "Grupo", "TAXA_APROVACAO": "Aprovação (%)"},
                template=CHART_THEME
            )
            fig_box_aprov.update_layout(showlegend=False, margin=dict(l=20, r=20, t=40, b=20), xaxis_title="")
            st.plotly_chart(fig_box_aprov, use_container_width=True)
            
        with col_d4:
            fig_box_ideb = px.box(
                sub.dropna(subset=["IDEB_OBSERVADO", "TIPO_GESTAO"]),
                x="TIPO_GESTAO",
                y="IDEB_OBSERVADO",
                color="TIPO_GESTAO",
                color_discrete_map=COLOR_MAP,
                points="outliers",
                title="Dispersão: IDEB Observado (0 a 10)",
                labels={"TIPO_GESTAO": "Grupo", "IDEB_OBSERVADO": "Nota IDEB"},
                template=CHART_THEME
            )
            fig_box_ideb.update_layout(showlegend=False, margin=dict(l=20, r=20, t=40, b=20), xaxis_title="")
            st.plotly_chart(fig_box_ideb, use_container_width=True)

    with tab_tab:
        tabela_dados = [
            {
                "Indicador": "Taxa de Aprovação Escolar (%)",
                "Média CCM": f"{m_aprov_ccm:.2f}%" if m_aprov_ccm is not None else "N/D",
                "N (CCM)": f"{len(aprov_ccm):,}",
                "Média Rede Regular": f"{m_aprov_reg:.2f}%" if m_aprov_reg is not None else "N/D",
                "N (Regular)": f"{len(aprov_reg):,}",
                "Diferença Absoluta (Δ)": f"{delta_aprov:+.2f} p.p." if delta_aprov is not None else "N/D",
                "Diferença Relativa (Δ%)": f"{(delta_aprov / m_aprov_reg * 100):+.2f}%" if (delta_aprov is not None and m_aprov_reg) else "N/D",
            },
            {
                "Indicador": "SAEB — Língua Portuguesa (Pontos)",
                "Média CCM": f"{m_lp_ccm:.2f}" if m_lp_ccm is not None else "N/D",
                "N (CCM)": f"{len(lp_ccm):,}",
                "Média Rede Regular": f"{m_lp_reg:.2f}" if m_lp_reg is not None else "N/D",
                "N (Regular)": f"{len(lp_reg):,}",
                "Diferença Absoluta (Δ)": f"{delta_lp:+.2f} pts" if delta_lp is not None else "N/D",
                "Diferença Relativa (Δ%)": f"{(delta_lp / m_lp_reg * 100):+.2f}%" if (delta_lp is not None and m_lp_reg) else "N/D",
            },
            {
                "Indicador": "SAEB — Matemática (Pontos)",
                "Média CCM": f"{m_mt_ccm:.2f}" if m_mt_ccm is not None else "N/D",
                "N (CCM)": f"{len(mt_ccm):,}",
                "Média Rede Regular": f"{m_mt_reg:.2f}" if m_mt_reg is not None else "N/D",
                "N (Regular)": f"{len(mt_reg):,}",
                "Diferença Absoluta (Δ)": f"{delta_mt:+.2f} pts" if delta_mt is not None else "N/D",
                "Diferença Relativa (Δ%)": f"{(delta_mt / m_mt_reg * 100):+.2f}%" if (delta_mt is not None and m_mt_reg) else "N/D",
            },
            {
                "Indicador": "IDEB Observado (0 a 10)",
                "Média CCM": f"{m_ideb_ccm:.2f}" if m_ideb_ccm is not None else "N/D",
                "N (CCM)": f"{len(ideb_ccm):,}",
                "Média Rede Regular": f"{m_ideb_reg:.2f}" if m_ideb_reg is not None else "N/D",
                "N (Regular)": f"{len(ideb_reg):,}",
                "Diferença Absoluta (Δ)": f"{delta_ideb:+.2f}" if delta_ideb is not None else "N/D",
                "Diferença Relativa (Δ%)": f"{(delta_ideb / m_ideb_reg * 100):+.2f}%" if (delta_ideb is not None and m_ideb_reg) else "N/D",
            }
        ]
        st.dataframe(pd.DataFrame(tabela_dados), use_container_width=True, hide_index=True)

    # Transparência e aprofundamento
    c_alert, c_btn_go = st.columns([3.5, 1.5])
    with c_alert:
        st.info(
            """
            ⚖️ **Nota de Rigor Metodológico e Jornalístico:**  
            As diferenças agregadas apresentadas acima são de natureza **estritamente descritiva** e retratam 
            os estabelecimentos da Rede Estadual no ciclo censitário selecionado. Elas incorporam trajetórias 
            históricas e perfis socioeconômicos prévios, **não devendo ser interpretadas isoladamente como 
            efeito causal ou impacto exclusivo do modelo cívico-militar**.
            """,
            icon="ℹ️"
        )
    with c_btn_go:
        st.write("")
        st.write("")
        if st.button("🔍 Aprofundar na Central de Comparações ➔", key="btn_goto_comparisons_from_overview", use_container_width=True, type="primary"):
            st.session_state["nav_tab"] = "Comparações"
            st.session_state["selected_inep"] = None
            if "escola" in st.query_params:
                del st.query_params["escola"]
            st.rerun()

def render_overview_view():
    st.header("📊 Visão Geral da Implantação dos Colégios Cívico-Militares")
    st.markdown(
        """
        Ambiente de monitoramento e análise descritiva da política de Colégios Cívico-Militares (CCM) 
        no Estado do Paraná. Os dados apresentados são derivados de auditoria documental exaustiva 
        dos atos oficiais publicados no Diário Oficial Executivo (DIOE/PR) e dos registros censitários do INEP.
        """
    )
    
    # Carregamento dos dados
    df_cad = load_cadastro()
    df_hist = load_historico_ano()
    
    # ==========================================
    # 1. RESUMO DA IMPLANTAÇÃO (MÉTRICAS DINÂMICAS)
    # ==========================================
    st.markdown("### 🏛️ Resumo da Implantação Documental")
    st.caption("Indicadores agregados a partir da base cadastral oficial auditada (sem valores fixos em código).")
    
    # Cálculos a partir da base
    total_base = len(df_cad)
    total_estaduais = len(df_cad[df_cad["dependencia_administrativa"] == "Estadual"])
    
    # Universo CCM auditado
    df_ccm_auditado = df_cad[df_cad["is_ccm"] == True]
    total_auditado = len(df_ccm_auditado)
    
    # Escolas por ano de início na base
    # status_ccm_atual: SIM (106 em 2024), FUTURO_2026 (33 em 2026), INDETERMINADO (62)
    ccm_2024 = len(df_cad[df_cad["ano_inicio_ccm"] == "2024"])
    ccm_2026 = len(df_cad[df_cad["ano_inicio_ccm"] == "2026"])
    ccm_confirmadas = ccm_2024 + ccm_2026
    ccm_indeterminado = len(df_cad[df_cad["ano_inicio_ccm"] == "INDETERMINADO"])
    
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric(
            label="Total de Escolas na Base",
            value=f"{total_base:,}",
            help=f"Total de estabelecimentos de ensino no Paraná catalogados pelo INEP (inclui {total_estaduais:,} da rede estadual)."
        )
        st.caption(f"**{total_estaduais:,}** na Rede Estadual")
        
    with c2:
        st.metric(
            label="CCM Confirmadas (Total)",
            value=f"{ccm_confirmadas:,}",
            help="Escolas com ato de homologação oficial publicado em Diário Oficial (lotes 2024 e 2026)."
        )
        st.caption(f"**{ccm_confirmadas/total_auditado*100:.1f}%** das escolas auditadas")
        
    with c3:
        st.metric(
            label="Início em 2024 (Ativas)",
            value=f"{ccm_2024:,}",
            help="Escolas que iniciaram operação no modelo cívico-militar no ano letivo de 2024 (Editais 107, 121 e 128/2023)."
        )
        st.caption("Em atividade no modelo")
        
    with c4:
        st.metric(
            label="Início em 2026 (Homologadas)",
            value=f"{ccm_2026:,}",
            help="Escolas com consulta homologada para início em 2026 (Edital 136/2025)."
        )
        st.caption("Homologação futura")
        
    with c5:
        st.metric(
            label="Status Indeterminado",
            value=f"{ccm_indeterminado:,}",
            help="Escolas selecionadas para consulta cujo processo resultou na manutenção do modelo regular (61 casos) ou erro documental retificado (1 caso)."
        )
        st.caption("Consultas não convertidas")

    st.divider()

    # ==========================================
    # 2. EVOLUÇÃO TEMPORAL (2020 - 2026)
    # ==========================================
    st.markdown("### 📈 Evolução Temporal dos Status Documentais (2020–2026)")
    st.markdown(
        """
        A matriz histórica anual acompanha a situação formal de cada uma das **201 escolas** que compõem o universo 
        de editais do programa ao longo de 7 anos letivos.
        """
    )
    
    # Agrupamento da matriz temporal por ano e civico_militar
    tab_status_ano = df_hist.groupby(["ano", "civico_militar"]).size().reset_index(name="quantidade")
    
    # Cores neutras e categóricas
    status_colors = {
        "SIM": "#1E3A8A",            # Azul escuro sóbrio
        "NAO": "#64748B",            # Slate neutro
        "INDETERMINADO": "#D97706"   # Âmbar / mostarda neutro
    }
    
    # Ordem das categorias
    tab_status_ano["civico_militar"] = pd.Categorical(
        tab_status_ano["civico_militar"], 
        categories=["SIM", "NAO", "INDETERMINADO"], 
        ordered=True
    )
    tab_status_ano = tab_status_ano.sort_values(["ano", "civico_militar"])
    
    fig_hist = px.bar(
        tab_status_ano,
        x="ano",
        y="quantidade",
        color="civico_militar",
        color_discrete_map=status_colors,
        barmode="stack",
        text="quantidade",
        title="Distribuição Anual do Status Documental das 201 Escolas Auditadas (2020 a 2026)",
        labels={
            "ano": "Ano Letivo",
            "quantidade": "Quantidade de Escolas",
            "civico_militar": "Status Documental"
        },
        template="plotly_white"
    )
    
    fig_hist.update_traces(textposition="inside", textfont_size=12)
    fig_hist.update_layout(
        xaxis=dict(tickmode="linear", dtick=1),
        yaxis_title="Número de Escolas",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    st.plotly_chart(fig_hist, use_container_width=True)
    
    # Alerta metodológico fundamental
    st.info(
        """
        ℹ️ **Nota Metodológica sobre o Status `INDETERMINADO`:**  
        O status **`INDETERMINADO`** significa **ausência de evidência documental suficiente** para determinar formalmente 
        o status naquele período específico (por exemplo: anos anteriores à deflagração dos primeiros editais de consulta, 
        de 2020 a 2022, ou escolas onde a comunidade escolar votou pela rejeição da transição).  
        **Não deve ser interpretado como ausência ou presença tácita do modelo**, mas sim como o limite estrito da comprovação documental auditada.
        """,
        icon="⚖️"
    )

    # Tabela detalhada de apoio
    with st.expander("📋 Ver Tabela Numérica Cruzada (Ano × Status Documental)"):
        pivot_hist = df_hist.pivot_table(
            index="ano", 
            columns="civico_militar", 
            values="codigo_inep", 
            aggfunc="count", 
            fill_value=0
        )[["SIM", "NAO", "INDETERMINADO"]]
        pivot_hist["Total Auditado"] = pivot_hist.sum(axis=1)
        st.dataframe(pivot_hist, use_container_width=True)

    st.divider()

    # ==========================================
    # 3. COMPARAÇÃO EDUCACIONAL: CCM VS. REGULAR
    # ==========================================
    render_overview_comparison_section()

    st.divider()

    # ==========================================
    # 4. DISTRIBUIÇÃO GEOGRÁFICA & NAVEGAÇÃO
    # ==========================================
    st.markdown("### 🗺️ Distribuição Geográfica no Território Paranaense")
    st.markdown(
        """
        As escolas que integraram processos de consulta e homologação para o modelo cívico-militar 
        estão distribuídas por dezenas de municípios em todas as macrorregiões do Paraná.
        """
    )
    
    col_geo1, col_geo2 = st.columns([3, 2])
    
    with col_geo1:
        # Mini-mapa interativo de prévia
        df_geo_ccm = df_cad[df_cad["is_ccm"] == True].copy()
        df_geo_ccm["Categoria"] = df_geo_ccm["status_ccm_atual"].map({
            "SIM": "CCM Ativa (Início 2024)",
            "FUTURO_2026": "CCM Homologada (Início 2026)",
            "INDETERMINADO": "Consulta Rejeitada / Sem Homologação"
        }).fillna("Outras")
        
        map_cat_colors = {
            "CCM Ativa (Início 2024)": "#1E3A8A",
            "CCM Homologada (Início 2026)": "#0284C7",
            "Consulta Rejeitada / Sem Homologação": "#D97706",
            "Outras": "#64748B"
        }
        
        map_kwargs = dict(
            data_frame=df_geo_ccm,
            lat="latitude",
            lon="longitude",
            color="Categoria",
            color_discrete_map=map_cat_colors,
            hover_name="nome_escola",
            hover_data={
                "municipio": True,
                "nre": True,
                "ano_inicio_ccm": True,
                "latitude": False,
                "longitude": False
            },
            zoom=5.5,
            center={"lat": -24.8, "lon": -51.6},
            title="Prévia Geográfica: Universo de 201 Escolas Auditadas",
            opacity=0.85
        )
        if hasattr(px, "scatter_map"):
            fig_prev = px.scatter_map(map_style="carto-positron", **map_kwargs)
        else:
            fig_prev = px.scatter_mapbox(mapbox_style="carto-positron", **map_kwargs)
            
        fig_prev.update_layout(
            margin=dict(l=10, r=10, t=40, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1)
        )
        st.plotly_chart(fig_prev, use_container_width=True)
        st.caption("📌 *Nota: 100% dos pontos CCM possuem coordenadas exatas auditadas a partir do arquivo KML oficial da SEED-PR.*")
        
    with col_geo2:
        st.markdown("#### Como Navegar pelo Painel")
        st.write(
            """
            Utilize os atalhos abaixo ou a barra de navegação superior para explorar os dados em detalhe:
            """
        )
        
        with st.container(border=True):
            st.markdown("##### 🗺️ **Mapa Interativo**")
            st.write("Visualize todas as escolas no mapa do Paraná com filtros territoriais, por NRE, etapa e ano de início.")
            if st.button("Ir para o Mapa Interativo ➔", key="btn_goto_map", use_container_width=True, type="primary"):
                st.session_state["nav_tab"] = "Mapa"
                st.session_state["selected_inep"] = None
                if "escola" in st.query_params:
                    del st.query_params["escola"]
                st.rerun()

        with st.container(border=True):
            st.markdown("##### 🏫 **Catálogo de Escolas**")
            st.write("Pesquise por qualquer escola ou código INEP, filtre por município ou status e acesse o raio-x detalhado.")
            if st.button("Ir para Lista de Escolas ➔", key="btn_goto_schools", use_container_width=True, type="primary"):
                st.session_state["nav_tab"] = "Escolas"
                st.session_state["selected_inep"] = None
                if "escola" in st.query_params:
                    del st.query_params["escola"]
                st.rerun()

        with st.container(border=True):
            st.markdown("##### 📈 **Evolução & Linha de Base**")
            st.write("Examine o perfil pré-intervenção das escolas e compare com o grupo de controle regular e escolas consultadas.")
            if st.button("Ir para Análise de Evolução ➔", key="btn_goto_evolution", use_container_width=True, type="primary"):
                st.session_state["nav_tab"] = "Evolução"
                st.session_state["selected_inep"] = None
                if "escola" in st.query_params:
                    del st.query_params["escola"]
                st.rerun()
