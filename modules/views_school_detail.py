import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from modules.data_loader import (
    load_cadastro,
    load_historico_ano,
    load_historico_eventos,
    load_saeb_tidy,
    load_rendimento_tidy,
    load_ideb_tidy
)

def render_school_detail_view(codigo_inep: int):
    """
    Renderiza o raio-x e histórico documental completo de uma escola por seu código INEP.
    """
    df_cad = load_cadastro()
    df_hist = load_historico_ano()
    df_ev = load_historico_eventos()
    df_saeb = load_saeb_tidy()
    df_rend = load_rendimento_tidy()
    df_ideb = load_ideb_tidy()
    
    # Busca da escola no cadastro
    esc_match = df_cad[df_cad["codigo_inep"] == codigo_inep]
    if esc_match.empty:
        st.error(f"Escola com código INEP {codigo_inep} não foi localizada na base de dados.")
        if st.button("⬅️ Voltar à Lista de Escolas"):
            st.session_state["selected_inep"] = None
            if "escola" in st.query_params:
                del st.query_params["escola"]
            st.rerun()
        return

    esc = esc_match.iloc[0]
    nome_escola = esc["nome_escola"]
    municipio = esc["municipio"]
    nre = esc.get("nre", "Não informado")
    if pd.isna(nre) or not str(nre).strip():
        nre = "Não informado"
        
    is_ccm = bool(esc.get("is_ccm", False))
    ano_inicio = esc.get("ano_inicio_ccm", None)
    ano_inicio_str = str(ano_inicio) if pd.notna(ano_inicio) and str(ano_inicio).strip() != "" else None
    
    # ==========================================
    # BARRA SUPERIOR DE NAVEGAÇÃO & ATALHOS
    # ==========================================
    c_back, c_quick_search = st.columns([2, 5])
    with c_back:
        if st.button("⬅️ Voltar à Lista / Mapa", use_container_width=True):
            st.session_state["selected_inep"] = None
            if "escola" in st.query_params:
                del st.query_params["escola"]
            st.rerun()
            
    with c_quick_search:
        # Seletor rápido para trocar de escola
        all_schools = df_cad.sort_values(["municipio", "nome_escola"])
        quick_opts = [
            f"{r['nome_escola']} — {r['municipio']} (INEP: {r['codigo_inep']})"
            for _, r in all_schools.head(250).iterrows()
        ]
        chosen_quick = st.selectbox(
            "Alternar rapidamente para outra escola:",
            options=["Selecione para navegar..."] + quick_opts,
            index=0,
            key="detail_quick_switch"
        )
        if chosen_quick != "Selecione para navegar...":
            new_inep = int(chosen_quick.split("INEP: ")[-1].replace(")", ""))
            if new_inep != codigo_inep:
                st.session_state["selected_inep"] = new_inep
                st.query_params["escola"] = str(new_inep)
                st.rerun()

    st.divider()

    # ==========================================
    # 1. IDENTIFICAÇÃO CADASTRAL COMPLETA
    # ==========================================
    st.markdown(f"## 🏫 {nome_escola}")
    
    # Badges cadastrais
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Código INEP", str(codigo_inep))
    k2.metric("Município", municipio)
    k3.metric("Núcleo Regional (NRE)", nre)
    k4.metric("Rede / Dependência", f"{esc['rede_ensino']}")
    
    # Metadados adicionais
    with st.container(border=True):
        m1, m2, m3, m4 = st.columns(4)
        m1.write(f"**Localização:** {esc.get('localizacao', 'Urbana')}")
        m2.write(f"**Situação:** {esc.get('situacao_funcionamento', 'EM_ATIVIDADE')}")
        m3.write(f"**Coordenadas:** `{esc['latitude']:.5f}, {esc['longitude']:.5f}`")
        m4.write(f"**Precisão:** `{esc['tipo_coordenada']}`")
        
        st.write(f"**Etapas Ofertadas:** *{esc.get('etapas_ofertadas', 'Não especificado')}*")
        if pd.notna(esc.get("nome_original_edital")) and str(esc.get("nome_original_edital")).strip():
            st.caption(f"Denominação no edital de origem: *{esc['nome_original_edital']}*")

    st.markdown("---")

    # ==========================================
    # 2. HISTÓRIA CCM: TIMELINE ANUAL (2020-2026)
    # ==========================================
    st.markdown("### 📜 História Documental CCM (2020–2026)")
    st.markdown(
        """
        Status formal de cada ano letivo de acordo com a matriz histórica auditada (`historico_ccm_por_ano.csv`).  
        *Nota: O status `INDETERMINADO` reflete ausência de evidência documental auditada no período, não significando presença ou ausência tácita.*
        """
    )
    
    hist_escola = df_hist[df_hist["codigo_inep"] == codigo_inep].sort_values("ano")
    
    if not hist_escola.empty:
        # Renderizar timeline visual em colunas
        anos_hist = hist_escola["ano"].tolist()
        cols_timeline = st.columns(len(anos_hist))
        
        status_badges = {
            "SIM": ("🛡️ SIM", "#1E3A8A", "Escola em operação sob modelo cívico-militar"),
            "NAO": ("🏛️ NAO", "#64748B", "Escola operando na rede regular"),
            "INDETERMINADO": ("❓ INDETERMINADO", "#D97706", "Ausência de evidência documental suficiente")
        }
        
        for idx, col in enumerate(cols_timeline):
            row_ano = hist_escola.iloc[idx]
            ano_val = row_ano["ano"]
            st_val = str(row_ano["civico_militar"]).strip()
            badge_text, badge_color, badge_tip = status_badges.get(
                st_val, (st_val, "#475569", "Sem informação")
            )
            
            with col:
                with st.container(border=True):
                    st.markdown(f"**{ano_val}**")
                    st.markdown(f"`{badge_text}`")
                    st.caption(f"*{row_ano.get('status_historico', '')[:30]}*")
                    
        # Rastreabilidade documental: Eventos e Atos
        ev_escola = df_ev[df_ev["codigo_inep_num"] == codigo_inep].sort_values("ano", ascending=False)
        
        if not ev_escola.empty:
            st.markdown("#### 📑 Atos e Eventos Oficiais Auditados")
            st.markdown("Rastreabilidade até o documento oficial publicado em Diário Oficial:")
            
            for _, ev_row in ev_escola.iterrows():
                with st.expander(
                    f"📄 {ev_row.get('documento_origem', 'Ato')} (Ano {ev_row.get('ano', '')}) — {ev_row.get('tipo_evento', '')}",
                    expanded=True
                ):
                    e1, e2, e3 = st.columns(3)
                    e1.write(f"**Tipo de Evento:** {ev_row.get('tipo_evento', '-')}")
                    e2.write(f"**Documento de Origem:** {ev_row.get('documento_origem', '-')}")
                    e3.write(f"**Página no Diário Oficial:** {ev_row.get('pagina_origem', '-')}")
                    
                    e4, e5, e6 = st.columns(3)
                    e4.write(f"**Data do Documento:** {ev_row.get('data_documento', '-')}")
                    e5.write(f"**Data do Evento:** {ev_row.get('data_evento', '-')}")
                    e6.write(f"**Nível de Confiança:** `{ev_row.get('nivel_confianca', 'CONFIRMADO')}`")
                    
                    if pd.notna(ev_row.get("evidencia")) and str(ev_row.get("evidencia")).strip():
                        st.info(f"**Evidência Documental:** {ev_row['evidencia']}")
                    if pd.notna(ev_row.get("observacao")) and str(ev_row.get("observacao")).strip():
                        st.caption(f"**Observação dos Auditores:** {ev_row['observacao']}")
        else:
            st.caption("ℹ️ *Esta escola não possui eventos de edital registrados na base de consulta cívico-militar.*")
    else:
        st.info("ℹ️ Escola da rede regular sem histórico documental no programa cívico-militar.")

    st.markdown("---")

    # ==========================================
    # 3. INDICADORES EDUCACIONAIS DA ESCOLA
    # ==========================================
    st.markdown("### 📊 Evolução dos Indicadores Educacionais")
    st.markdown(
        """
        Séries históricas oficiais divulgadas pelo INEP/MEC.  
        *Valores ausentes (não participação, resultado não divulgado ou ausência de avaliação) são preservados como ausência, nunca como zero.*
        """
    )
    
    # Carregar dados da escola
    saeb_escola = df_saeb[df_saeb["ID_ESCOLA"] == codigo_inep].sort_values("ANO_SAEB")
    rend_escola = df_rend[df_rend["ID_ESCOLA"] == codigo_inep].sort_values("ANO")
    ideb_escola = df_ideb[df_ideb["ID_ESCOLA"] == codigo_inep].sort_values("ANO_IDEB")
    
    # Identificar etapas com dados
    etapas_saeb = saeb_escola["ETAPA"].dropna().unique().tolist()
    etapas_rend = rend_escola["ETAPA"].dropna().unique().tolist()
    etapas_ideb = ideb_escola["ETAPA"].dropna().unique().tolist()
    todas_etapas = sorted(list(set(etapas_saeb + etapas_rend + etapas_ideb)))
    
    if not todas_etapas:
        st.warning("Não há registros de avaliações do SAEB, Rendimento ou IDEB para este código INEP nas bases auditadas.")
        return
        
    # Seletor de etapa de ensino
    etapa_ativa = st.selectbox(
        "Selecione a Etapa de Ensino para Visualização dos Indicadores:",
        options=todas_etapas,
        index=0,
        help="As avaliações e taxas são mensuradas por etapa de ensino separadamente."
    )
    
    # Filtrar dados para a etapa ativa
    sub_saeb = saeb_escola[saeb_escola["ETAPA"] == etapa_ativa].copy()
    sub_rend = rend_escola[rend_escola["ETAPA"] == etapa_ativa].copy()
    sub_ideb = ideb_escola[ideb_escola["ETAPA"] == etapa_ativa].copy()
    
    # Identificar ano de início para marcação vertical
    ano_marca_inicio = None
    if ano_inicio_str in ["2024", "2026"]:
        ano_marca_inicio = int(ano_inicio_str)

    # ------------------------------------------
    # SUB-SEÇÃO A: SAEB (PORTUGUÊS E MATEMÁTICA)
    # ------------------------------------------
    st.markdown("#### 🎯 SAEB — Proficiências Médias Padronizadas")
    st.caption("Escala Saeb (0 a 500 pontos). Ausências de resultado correspondem a não divulgação por quórum ou não participação.")
    
    # Tratar ausências
    sub_saeb["SAEB_PORTUGUES"] = pd.to_numeric(sub_saeb["SAEB_PORTUGUES"], errors="coerce")
    sub_saeb["SAEB_MATEMATICA"] = pd.to_numeric(sub_saeb["SAEB_MATEMATICA"], errors="coerce")
    
    c_saeb1, c_saeb2 = st.columns(2)
    
    with c_saeb1:
        # Gráfico de Língua Portuguesa
        df_lp = sub_saeb.dropna(subset=["SAEB_PORTUGUES"])
        if not df_lp.empty:
            fig_lp = px.line(
                df_lp,
                x="ANO_SAEB",
                y="SAEB_PORTUGUES",
                markers=True,
                title=f"Língua Portuguesa — {etapa_ativa}",
                labels={"ANO_SAEB": "Ano da Edição Saeb", "SAEB_PORTUGUES": "Proficiência Média"},
                template="plotly_white"
            )
            fig_lp.update_traces(line_color="#2563EB", marker=dict(size=8, color="#1D4ED8"))
            fig_lp.update_layout(xaxis=dict(tickmode="linear", dtick=2))
            
            # Linha vertical discreta de início CCM quando aplicável
            if ano_marca_inicio:
                fig_lp.add_vline(
                    x=ano_marca_inicio,
                    line_dash="dot",
                    line_color="#475569",
                    line_width=2,
                    annotation_text=f"INÍCIO CCM {ano_marca_inicio}",
                    annotation_position="top left"
                )
            st.plotly_chart(fig_lp, use_container_width=True)
        else:
            st.info("Sem dados de proficiência em Língua Portuguesa divulgados para esta etapa.")
            
    with c_saeb2:
        # Gráfico de Matemática
        df_mat = sub_saeb.dropna(subset=["SAEB_MATEMATICA"])
        if not df_mat.empty:
            fig_mat = px.line(
                df_mat,
                x="ANO_SAEB",
                y="SAEB_MATEMATICA",
                markers=True,
                title=f"Matemática — {etapa_ativa}",
                labels={"ANO_SAEB": "Ano da Edição Saeb", "SAEB_MATEMATICA": "Proficiência Média"},
                template="plotly_white"
            )
            fig_mat.update_traces(line_color="#0D9488", marker=dict(size=8, color="#0F766E"))
            fig_mat.update_layout(xaxis=dict(tickmode="linear", dtick=2))
            
            if ano_marca_inicio:
                fig_mat.add_vline(
                    x=ano_marca_inicio,
                    line_dash="dot",
                    line_color="#475569",
                    line_width=2,
                    annotation_text=f"INÍCIO CCM {ano_marca_inicio}",
                    annotation_position="top left"
                )
            st.plotly_chart(fig_mat, use_container_width=True)
        else:
            st.info("Sem dados de proficiência em Matemática divulgados para esta etapa.")

    # Status de participação nos anos
    with st.expander("ℹ️ Detalhes de Participação e Critérios de Divulgação SAEB"):
        st.dataframe(
            sub_saeb[["ANO_SAEB", "SAEB_PORTUGUES", "SAEB_MATEMATICA", "SAEB_NOTA_MEDIA", "STATUS_PARTICIPACAO_SAEB"]].rename(
                columns={
                    "ANO_SAEB": "Ano SAEB",
                    "SAEB_PORTUGUES": "Língua Portuguesa",
                    "SAEB_MATEMATICA": "Matemática",
                    "SAEB_NOTA_MEDIA": "Nota Média (0-10)",
                    "STATUS_PARTICIPACAO_SAEB": "Status de Divulgação"
                }
            ),
            use_container_width=True,
            hide_index=True
        )

    # ------------------------------------------
    # SUB-SEÇÃO B: RENDIMENTO (APROVAÇÃO, REPROVAÇÃO, ABANDONO)
    # ------------------------------------------
    st.markdown("#### 📋 Rendimento Escolar (Fluxo)")
    st.caption("Taxas anuais apuradas pelo Censo Escolar da Educação Básica (2017 a 2023).")
    
    sub_rend["TAXA_APROVACAO"] = pd.to_numeric(sub_rend["TAXA_APROVACAO"], errors="coerce")
    sub_rend["TAXA_REPROVACAO"] = pd.to_numeric(sub_rend["TAXA_REPROVACAO"], errors="coerce")
    sub_rend["TAXA_ABANDONO"] = pd.to_numeric(sub_rend["TAXA_ABANDONO"], errors="coerce")
    
    df_rend_valid = sub_rend.dropna(subset=["TAXA_APROVACAO"])
    
    if not df_rend_valid.empty:
        fig_rend = go.Figure()
        
        # Aprovação
        fig_rend.add_trace(go.Scatter(
            x=df_rend_valid["ANO"],
            y=df_rend_valid["TAXA_APROVACAO"],
            mode="lines+markers",
            name="Taxa de Aprovação (%)",
            line=dict(color="#16A34A", width=3),
            marker=dict(size=7)
        ))
        
        # Reprovação
        fig_rend.add_trace(go.Scatter(
            x=df_rend_valid["ANO"],
            y=df_rend_valid["TAXA_REPROVACAO"],
            mode="lines+markers",
            name="Taxa de Reprovação (%)",
            line=dict(color="#EA580C", width=2),
            marker=dict(size=6)
        ))
        
        # Abandono
        fig_rend.add_trace(go.Scatter(
            x=df_rend_valid["ANO"],
            y=df_rend_valid["TAXA_ABANDONO"],
            mode="lines+markers",
            name="Taxa de Abandono (%)",
            line=dict(color="#DC2626", width=2),
            marker=dict(size=6)
        ))
        
        if ano_marca_inicio:
            fig_rend.add_vline(
                x=ano_marca_inicio,
                line_dash="dot",
                line_color="#475569",
                line_width=2,
                annotation_text=f"INÍCIO CCM {ano_marca_inicio}",
                annotation_position="top left"
            )
            
        fig_rend.update_layout(
            title=f"Fluxo Escolar: Aprovação, Reprovação e Abandono (2017 a 2023) — {etapa_ativa}",
            xaxis=dict(tickmode="linear", dtick=1, title="Ano Letivo"),
            yaxis=dict(title="Taxa (%)", range=[0, 105]),
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_rend, use_container_width=True)
    else:
        st.info("Sem dados de rendimento escolar disponíveis para esta etapa.")

    # ------------------------------------------
    # SUB-SEÇÃO C: IDEB (OBSERVADO VS META)
    # ------------------------------------------
    st.markdown("#### 📈 Série Histórica do IDEB")
    st.caption("Índice de Desenvolvimento da Educação Básica (0 a 10) divulgado pelo INEP.")
    
    sub_ideb["IDEB_OBSERVADO"] = pd.to_numeric(sub_ideb["IDEB_OBSERVADO"], errors="coerce")
    sub_ideb["IDEB_META"] = pd.to_numeric(sub_ideb["IDEB_META"], errors="coerce")
    
    df_ideb_valid = sub_ideb.dropna(subset=["IDEB_OBSERVADO"])
    
    if not df_ideb_valid.empty:
        fig_ideb = go.Figure()
        
        # IDEB Observado
        fig_ideb.add_trace(go.Scatter(
            x=df_ideb_valid["ANO_IDEB"],
            y=df_ideb_valid["IDEB_OBSERVADO"],
            mode="lines+markers",
            name="IDEB Observado",
            line=dict(color="#1E3A8A", width=3),
            marker=dict(size=8)
        ))
        
        # Meta projetada quando disponível
        df_meta_valid = sub_ideb.dropna(subset=["IDEB_META"])
        if not df_meta_valid.empty:
            fig_ideb.add_trace(go.Scatter(
                x=df_meta_valid["ANO_IDEB"],
                y=df_meta_valid["IDEB_META"],
                mode="lines+markers",
                name="Meta Projetada (MEC)",
                line=dict(color="#D97706", width=2, dash="dash"),
                marker=dict(size=6)
            ))
            
        if ano_marca_inicio:
            fig_ideb.add_vline(
                x=ano_marca_inicio,
                line_dash="dot",
                line_color="#475569",
                line_width=2,
                annotation_text=f"INÍCIO CCM {ano_marca_inicio}",
                annotation_position="top left"
            )
            
        fig_ideb.update_layout(
            title=f"IDEB Observado vs Meta Projetada (2005 a 2023) — {etapa_ativa}",
            xaxis=dict(tickmode="linear", dtick=2, title="Ano da Edição"),
            yaxis=dict(title="Índice (0 a 10)"),
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_ideb, use_container_width=True)
    else:
        st.info("Sem dados de IDEB Observado para esta etapa de ensino.")

    # ==========================================
    # 4. TABELA CONSOLIDADA DE TODOS OS ANOS
    # ==========================================
    with st.expander("📋 Tabela Consolidada de Indicadores Históricos"):
        # Fazer merge dos dados das 3 fontes para visualização analítica
        tab_saeb_sub = sub_saeb[["ANO_SAEB", "SAEB_PORTUGUES", "SAEB_MATEMATICA", "SAEB_NOTA_MEDIA"]].rename(columns={"ANO_SAEB": "ANO"})
        tab_rend_sub = sub_rend[["ANO", "TAXA_APROVACAO", "TAXA_REPROVACAO", "TAXA_ABANDONO"]]
        tab_ideb_sub = sub_ideb[["ANO_IDEB", "IDEB_OBSERVADO", "IDEB_META"]].rename(columns={"ANO_IDEB": "ANO"})
        
        tab_merged = pd.merge(tab_saeb_sub, tab_rend_sub, on="ANO", how="outer")
        tab_merged = pd.merge(tab_merged, tab_ideb_sub, on="ANO", how="outer").sort_values("ANO")
        
        st.dataframe(
            tab_merged.style.format({
                "SAEB_PORTUGUES": "{:.1f}",
                "SAEB_MATEMATICA": "{:.1f}",
                "SAEB_NOTA_MEDIA": "{:.2f}",
                "TAXA_APROVACAO": "{:.1f}%",
                "TAXA_REPROVACAO": "{:.1f}%",
                "TAXA_ABANDONO": "{:.1f}%",
                "IDEB_OBSERVADO": "{:.2f}",
                "IDEB_META": "{:.2f}"
            }, na_rep="-"),
            use_container_width=True,
            hide_index=True
        )
