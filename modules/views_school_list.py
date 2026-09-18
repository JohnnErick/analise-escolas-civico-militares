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
            
        st.markdown("##### 🔀 Ordenação da Lista *(Critérios Neutros)*")
        ordem_col, _ = st.columns([2, 2])
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
    
    st.info("💡 **Dica:** Clique em uma linha da tabela abaixo para inspecionar os dados ou utilize a busca rápida para abrir diretamente o relatório da unidade.")
    
    # Evento de seleção na tabela interativa
    event = st.dataframe(
        tabela_show,
        use_container_width=True,
        height=480,
        selection_mode="single-row",
        on_select="rerun",
        hide_index=True,
        key="table_schools_main"
    )
    
    selected_row_inep = None
    if event and event.selection and event.selection.rows:
        sel_idx = event.selection.rows[0]
        selected_row_inep = int(df_filtered.iloc[sel_idx]["codigo_inep"])
        
    # Seletor alternativo explícito
    c_btn1, c_btn2 = st.columns([3, 1])
    with c_btn1:
        if selected_row_inep:
            row_esc = df_filtered[df_filtered["codigo_inep"] == selected_row_inep].iloc[0]
            st.success(f"Escola selecionada: **{row_esc['nome_escola']}** (INEP: {selected_row_inep})")
        else:
            # Dropdown de atalho rápido
            opcoes_rapidas = [
                f"{r['nome_escola']} — {r['municipio']} (INEP: {r['codigo_inep']})"
                for _, r in df_filtered.head(100).iterrows()
            ]
            escolha_drop = st.selectbox(
                "Ou escolha diretamente uma escola da lista filtrada:",
                options=["Selecione para abrir o detalhe..."] + opcoes_rapidas,
                index=0
            )
            if escolha_drop != "Selecione para abrir o detalhe...":
                selected_row_inep = int(escolha_drop.split("INEP: ")[-1].replace(")", ""))
                
    with c_btn2:
        st.write("")
        st.write("")
        if selected_row_inep:
            if st.button("🔍 Ver Detalhes da Escola ➔", key="btn_open_selected_detail", use_container_width=True):
                st.session_state["selected_inep"] = selected_row_inep
                st.query_params["escola"] = str(selected_row_inep)
                st.rerun()
