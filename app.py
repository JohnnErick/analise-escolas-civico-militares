import sys
import importlib
import streamlit as st
import pandas as pd

# Recarrega submódulos locais caso o processo do Streamlit já os tenha em memória
for _mod in [
    "modules.data_loader",
    "modules.components",
    "modules.charts",
    "modules.views_overview",
    "modules.views_map",
    "modules.views_school_list",
    "modules.views_school_detail",
    "modules.views_comparisons",
    "modules.views_evolution",
    "modules.views_methodology",
    "modules.views_transparency"
]:
    if _mod in sys.modules:
        try:
            importlib.reload(sys.modules[_mod])
        except Exception:
            pass

from modules.components import render_header, render_investigation_banner
from modules.views_overview import render_overview_view
from modules.views_map import render_map_view
from modules.views_school_list import render_school_list_view
from modules.views_school_detail import render_school_detail_view
from modules.views_comparisons import render_comparisons_view
from modules.views_evolution import render_evolution_view
from modules.views_methodology import render_methodology_view
from modules.views_transparency import render_transparency_view
from modules.data_loader import load_cadastro

# Configuração da página
st.set_page_config(
    page_title="Painel de Investigação: Colégios Cívico-Militares do Paraná",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    render_header()
    render_investigation_banner()
    
    # Gerenciamento de roteamento por Query Params e Session State
    query_inep = st.query_params.get("escola") or st.query_params.get("inep")
    if "selected_inep" not in st.session_state:
        st.session_state["selected_inep"] = None
        
    if query_inep and str(query_inep).isdigit():
        st.session_state["selected_inep"] = int(query_inep)
        
    # ==========================================
    # SIDEBAR: NAVEGAÇÃO & BUSCA GLOBAL
    # ==========================================
    st.sidebar.title("🏫 Investigação CCM-PR")
    st.sidebar.caption("Dados Oficiais Auditados — Estado do Paraná")
    
    # Busca Global Rápida por Escola / INEP
    st.sidebar.markdown("---")
    st.sidebar.markdown("##### 🔍 Busca Direta de Escola")
    
    try:
        df_cad = load_cadastro()
        lista_busca = [
            f"{r['nome_escola']} — {r['municipio']} (INEP: {r['codigo_inep']})"
            for _, r in df_cad.sort_values(["municipio", "nome_escola"]).iterrows()
        ]
        busca_global = st.sidebar.selectbox(
            "Localizar qualquer escola:",
            options=["Digite ou selecione uma escola..."] + lista_busca,
            index=0,
            key="sidebar_global_school_search"
        )
        if busca_global != "Digite ou selecione uma escola...":
            inep_buscado = int(busca_global.split("INEP: ")[-1].replace(")", ""))
            if st.session_state["selected_inep"] != inep_buscado:
                st.session_state["selected_inep"] = inep_buscado
                st.query_params["escola"] = str(inep_buscado)
                st.rerun()
    except Exception as e:
        st.sidebar.warning("Carregamento cadastral em andamento...")
        
    st.sidebar.markdown("---")
    st.sidebar.markdown("##### 🧭 Navegação Principal")
    
    nav_options = [
        "Visão geral",
        "Mapa",
        "Escolas",
        "Comparações",
        "Evolução",
        "Metodologia",
        "Dados"
    ]
    
    # Se o usuário estava em uma aba anterior gravada
    if "nav_tab" not in st.session_state or st.session_state["nav_tab"] not in nav_options:
        st.session_state["nav_tab"] = "Visão geral"
        
    selected_nav = st.sidebar.radio(
        "Selecione uma área:",
        options=nav_options,
        index=nav_options.index(st.session_state["nav_tab"]),
        key="main_nav_radio"
    )
    st.session_state["nav_tab"] = selected_nav

    # Se estiver em modo de Detalhe da Escola e o usuário clicar em uma área do menu, sai do detalhe
    if st.session_state["selected_inep"] is not None:
        if st.sidebar.button("⬅️ Sair do Detalhe da Escola", use_container_width=True):
            st.session_state["selected_inep"] = None
            if "escola" in st.query_params:
                del st.query_params["escola"]
            st.rerun()

    # Informações de transparência no rodapé da barra lateral
    st.sidebar.markdown("---")
    st.sidebar.caption(
        "⚖️ **Princípio Jornalístico:** O painel reporta fatos e evidências documentais auditadas. "
        "Não gera conclusões causais, rankings ou escores de desempenho."
    )
    st.sidebar.caption("Versão auditada: `v1.2 (18/09/2026)`")

    # ==========================================
    # ROTEAMENTO E RENDERIZAÇÃO DE TELAS
    # ==========================================
    # Prioridade 1: Detalhe da Escola (se selecionada via URL, mapa, lista ou busca)
    if st.session_state["selected_inep"] is not None:
        render_school_detail_view(st.session_state["selected_inep"])
        return
        
    # Prioridade 2: Navegação principal entre as 7 áreas
    if selected_nav == "Visão geral":
        render_overview_view()
    elif selected_nav == "Mapa":
        render_map_view()
    elif selected_nav == "Escolas":
        render_school_list_view()
    elif selected_nav == "Comparações":
        render_comparisons_view()
    elif selected_nav == "Evolução":
        render_evolution_view()
    elif selected_nav == "Metodologia":
        render_methodology_view()
    elif selected_nav == "Dados":
        render_transparency_view()

if __name__ == "__main__":
    main()
