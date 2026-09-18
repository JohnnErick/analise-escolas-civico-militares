import streamlit as st
import pandas as pd
import numpy as np
from modules.data_loader import load_cadastro, load_historico_ano

def render_school_list_view():
    st.header("🏫 Lista & Catálogo de Escolas do Paraná")
    st.markdown(
        """
        Consulte e filtre individualmente os estabelecimentos de ensino do Paraná. 
        A tabela permite localizar qualquer unidade por nome, código INEP, município ou NRE, 
        e acessar o raio-x histórico e documental completo.
        """
    )
    
    # Carregamento de dados
    df_cad = load_cadastro()
    df_hist = load_historico_ano()
    
    # Adicionar status do ano mais recente (2024 ou 2026)
    hist_2024 = df_hist[df_hist["ano"] == 2024][["codigo_inep", "civico_militar"]].rename(
        columns={"civico_militar": "status_ccm_2024"}
    )
    df_view = df_cad.merge(hist_2024, on="codigo_inep", how="left")
    df_view["status_ccm_2024"] = df_view["status_ccm_2024"].fillna("NAO_CCM")
    
    # ==========================================
    # FILTROS DE BUSCA E NAVEGAÇÃO
    # ==========================================
    with st.expander("🎛️ Filtros de Pesquisa", expanded=True):
        c1, c2, c3 = st.columns([3, 2, 2])
        with c1:
            search_query = st.text_input(
                "🔍 Buscar por Nome da Escola ou Código INEP:",
                placeholder="Ex: Alberto Krause, 41122801...",
                key="school_list_search"
            ).strip().lower()
            
        with c2:
            escopo_list = st.selectbox(
                "Escopo de Gestão:",
                options=[
                    "Universo Auditado CCM (201 escolas)",
                    "Rede Estadual (2.017 escolas)",
                    "Todas as Escolas do Paraná (5.966 estabelecimentos)"
                ],
                index=0,
                key="school_list_escopo"
            )
            
        with c3:
            status_opt = st.selectbox(
                "Status CCM (Referência 2024):",
                options=["Todos", "SIM", "NAO", "INDETERMINADO", "NAO_CCM"],
                index=0,
                key="school_list_status"
            )
            
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            municipios_disponiveis = ["Todos os Municípios"] + sorted(df_cad["municipio"].dropna().unique().tolist())
            mun_opt = st.selectbox(
                "Município:",
                options=municipios_disponiveis,
                index=0,
                key="school_list_mun"
            )
        with f2:
            nres_disponiveis = ["Todos os NREs"] + sorted([str(n) for n in df_cad["nre"].dropna().unique() if str(n).strip()])
            nre_opt = st.selectbox(
                "NRE:",
                options=nres_disponiveis,
                index=0,
                key="school_list_nre"
            )
        with f3:
            etapa_opt = st.selectbox(
                "Etapa de Ensino:",
                options=["Todas as Etapas", "Anos Finais (6º-9º)", "Ensino Médio", "Anos Iniciais (1º-5º)"],
                index=0,
                key="school_list_etapa"
            )
        with f4:
            ano_ini_opt = st.selectbox(
                "Ano de Início CCM:",
                options=["Todos", "2024", "2026", "INDETERMINADO", "Regular (Sem CCM)"],
                index=0,
                key="school_list_ano_ini"
            )
            
        st.markdown("##### 🔀 Ordenação e Ações Rápidas")
        ordem_col, reset_col = st.columns([3, 1])
        with ordem_col:
            sort_choice = st.selectbox(
                "Ordenar por:",
                options=[
                    "Nome da Escola (A-Z)",
                    "Município (A-Z)",
                    "Código INEP (Crescente)",
                    "Ano de Início CCM (Crescente)"
                ],
                index=0,
                help="Ordenações restritas a critérios neutros. Não são permitidas ordenações baseadas em notas ou rankings."
            )
        with reset_col:
            st.write("")
            st.write("")
            if st.button("🧹 Limpar Filtros", key="btn_reset_school_filters", use_container_width=True):
                for k in ["school_list_search", "school_list_escopo", "school_list_status", "school_list_mun", "school_list_nre", "school_list_etapa", "school_list_ano_ini"]:
                    if k in st.session_state:
                        del st.session_state[k]
                st.session_state["school_list_page"] = 1
                st.rerun()

    # ==========================================
    # APLICAÇÃO DOS FILTROS
    # ==========================================
    df_filtered = df_view.copy()
    
    if escopo_list == "Universo Auditado CCM (201 escolas)":
        df_filtered = df_filtered[df_filtered["is_ccm"] == True]
    elif escopo_list == "Rede Estadual (2.017 escolas)":
        df_filtered = df_filtered[df_filtered["dependencia_administrativa"] == "Estadual"]
        
    if search_query:
        cond_nome = df_filtered["nome_escola"].astype(str).str.lower().str.contains(search_query, na=False)
        cond_inep = df_filtered["codigo_inep"].astype(str).str.contains(search_query, na=False)
        df_filtered = df_filtered[cond_nome | cond_inep]
        
    if status_opt != "Todos":
        df_filtered = df_filtered[df_filtered["status_ccm_2024"] == status_opt]
        
    if mun_opt != "Todos os Municípios":
        df_filtered = df_filtered[df_filtered["municipio"] == mun_opt]
        
    if nre_opt != "Todos os NREs":
        df_filtered = df_filtered[df_filtered["nre"] == nre_opt]
        
    if etapa_opt != "Todas as Etapas":
        df_filtered = df_filtered[df_filtered["etapas_ofertadas"].str.contains(etapa_opt, na=False)]
        
    if ano_ini_opt != "Todos":
        if ano_ini_opt == "Regular (Sem CCM)":
            df_filtered = df_filtered[df_filtered["ano_inicio_ccm"].isna()]
        else:
            df_filtered = df_filtered[df_filtered["ano_inicio_ccm"] == ano_ini_opt]

    # Ordenação estritamente neutra
    if sort_choice == "Nome da Escola (A-Z)":
        df_filtered = df_filtered.sort_values("nome_escola")
    elif sort_choice == "Município (A-Z)":
        df_filtered = df_filtered.sort_values(["municipio", "nome_escola"])
    elif sort_choice == "Código INEP (Crescente)":
        df_filtered = df_filtered.sort_values("codigo_inep")
    elif sort_choice == "Ano de Início CCM (Crescente)":
        df_filtered = df_filtered.sort_values(["ano_inicio_ccm", "nome_escola"], ascending=[True, True])

    total_encontrado = len(df_filtered)
    st.write(f"Exibindo **{total_encontrado:,}** escolas correspondentes aos filtros aplicados.")
    
    if total_encontrado == 0:
        st.warning("Nenhuma escola encontrada para os critérios selecionados.")
        return

    # Preparar tabela formatada
    # Colunas mínimas: Escola, INEP, Município, NRE, Etapa, Ano início CCM, Status CCM
    tabela_show = df_filtered[[
        "codigo_inep",
        "nome_escola",
        "municipio",
        "nre",
        "etapas_ofertadas",
        "ano_inicio_ccm",
        "status_ccm_2024",
        "rede_ensino"
    ]].copy()
    
    tabela_show["nre"] = tabela_show["nre"].fillna("Não informado")
    tabela_show["ano_inicio_ccm"] = tabela_show["ano_inicio_ccm"].fillna("Não se aplica")
    
    tabela_show = tabela_show.rename(columns={
        "nome_escola": "Escola",
        "codigo_inep": "INEP",
        "municipio": "Município",
        "nre": "NRE",
        "etapas_ofertadas": "Etapa",
        "ano_inicio_ccm": "Ano início CCM",
        "status_ccm_2024": "Status CCM (2024)",
        "rede_ensino": "Rede"
    })
    
    # ==========================================
    # LISTA DE ESCOLAS COM ACESSO DIRETO EM 1 CLIQUE
    # ==========================================
    st.markdown("---")
    st.markdown("### 📋 Escolas Encontradas")
    st.caption("Acesse instantaneamente o dossiê detalhado com raio-x de qualquer unidade clicando no botão correspondente:")
    
    PAGE_SIZE = 15
    total_pages = max(1, int(np.ceil(total_encontrado / PAGE_SIZE)))
    
    if "school_list_page" not in st.session_state:
        st.session_state["school_list_page"] = 1
        
    if st.session_state["school_list_page"] > total_pages:
        st.session_state["school_list_page"] = total_pages
    if st.session_state["school_list_page"] < 1:
        st.session_state["school_list_page"] = 1
        
    current_page = st.session_state["school_list_page"]
    
    # Barra superior de paginação (quando há múltiplas páginas)
    if total_pages > 1:
        col_p1, col_p2, col_p3 = st.columns([1, 2, 1])
        with col_p1:
            if st.button("◀️ Página Anterior", key="btn_prev_page_top", disabled=(current_page <= 1), use_container_width=True):
                st.session_state["school_list_page"] = current_page - 1
                st.rerun()
        with col_p2:
            st.markdown(
                f"<div style='text-align: center; padding-top: 6px; font-size: 0.9em;'>"
                f"Página <b>{current_page}</b> de <b>{total_pages}</b> &bull; "
                f"Exibindo <b>{(current_page - 1) * PAGE_SIZE + 1}</b> a <b>{min(current_page * PAGE_SIZE, total_encontrado)}</b> de <b>{total_encontrado}</b>"
                f"</div>",
                unsafe_allow_html=True
            )
        with col_p3:
            if st.button("Próxima Página ▶️", key="btn_next_page_top", disabled=(current_page >= total_pages), use_container_width=True):
                st.session_state["school_list_page"] = current_page + 1
                st.rerun()
                
    start_idx = (current_page - 1) * PAGE_SIZE
    end_idx = min(start_idx + PAGE_SIZE, total_encontrado)
    page_schools = df_filtered.iloc[start_idx:end_idx]
    
    # Renderização dos cards individuais com botão de 1 clique
    for _, row_esc in page_schools.iterrows():
        inep = int(row_esc["codigo_inep"])
        nome = row_esc["nome_escola"]
        mun = row_esc["municipio"]
        nre = row_esc.get("nre", "Não informado")
        rede = row_esc.get("rede_ensino", "Estadual")
        etapa = row_esc.get("etapas_ofertadas", "Não informada")
        is_ccm_flag = bool(row_esc.get("is_ccm", False))
        ano_ini = row_esc.get("ano_inicio_ccm")
        
        if is_ccm_flag:
            ini_txt = f" (Início: {ano_ini})" if pd.notna(ano_ini) and str(ano_ini).strip() and str(ano_ini) != "Não se aplica" else " (Auditada)"
            badge_html = f"<span style='background-color: #DCFCE7; color: #166534; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 0.85em;'>🟢 Cívico-Militar{ini_txt}</span>"
        else:
            badge_html = "<span style='background-color: #F1F5F9; color: #475569; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 0.85em;'>⚪ Regular (Sem CCM)</span>"
            
        with st.container(border=True):
            c_info, c_action = st.columns([3.5, 1.2])
            with c_info:
                st.markdown(f"#### 🏫 {nome}")
                st.markdown(
                    f"{badge_html} &nbsp;|&nbsp; 📍 **{mun}** (NRE: {nre}) &nbsp;|&nbsp; "
                    f"INEP: `{inep}` &nbsp;|&nbsp; Rede: **{rede}**",
                    unsafe_allow_html=True
                )
                if pd.notna(etapa) and str(etapa).strip():
                    st.caption(f"📚 Etapas: {etapa}")
            with c_action:
                st.write("")
                if st.button("🔍 Ver Raio-X ➔", key=f"btn_open_school_{inep}", type="primary", use_container_width=True):
                    st.session_state["selected_inep"] = inep
                    st.query_params["escola"] = str(inep)
                    st.rerun()

    # Barra inferior de paginação (quando há múltiplas páginas)
    if total_pages > 1:
        st.markdown("")
        col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
        with col_b1:
            if st.button("◀️ Página Anterior", key="btn_prev_page_bottom", disabled=(current_page <= 1), use_container_width=True):
                st.session_state["school_list_page"] = current_page - 1
                st.rerun()
        with col_b2:
            st.markdown(
                f"<div style='text-align: center; padding-top: 6px; font-size: 0.9em;'>"
                f"Página <b>{current_page}</b> de <b>{total_pages}</b>"
                f"</div>",
                unsafe_allow_html=True
            )
        with col_b3:
            if st.button("Próxima Página ▶️", key="btn_next_page_bottom", disabled=(current_page >= total_pages), use_container_width=True):
                st.session_state["school_list_page"] = current_page + 1
                st.rerun()

    # ==========================================
    # VISUALIZAÇÃO TABULAR PARA MICRODADOS E EXPORTAÇÃO
    # ==========================================
    st.markdown("---")
    with st.expander("📋 Ver Tabela Completa para Exportação e Microdados", expanded=False):
        st.caption(
            "Consulte ou baixe a listagem tabular completa de todas as escolas filtradas "
            "através dos controles nativos da tabela (ícone de download no canto superior direito)."
        )
        st.dataframe(
            tabela_show,
            use_container_width=True,
            height=400,
            hide_index=True,
            key="table_schools_export"
        )
