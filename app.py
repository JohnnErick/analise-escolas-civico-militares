import streamlit as st
import pandas as pd
from modules.data_loader import load_tidy_data, get_filter_options, apply_filters
from modules.components import render_header, render_investigation_banner
from modules.views_saeb import render_saeb_view
from modules.views_temporal import render_temporal_view
from modules.views_complementary import render_complementary_view
from modules.views_geo import render_geo_view
from modules.views_explorer import render_explorer_view
from modules.views_methodology import render_methodology_view

# Configuração da página
st.set_page_config(
    page_title="Painel de Análise: Escolas Cívico-Militares",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    render_header()
    render_investigation_banner()
    
    # Carregamento de dados com cache
    try:
        df_raw = load_tidy_data()
    except Exception as e:
        st.error(f"Erro ao carregar os dados estruturados: {e}")
        st.stop()
        
    filter_opts = get_filter_options(df_raw)
    
    # ==========================================
    # SIDEBAR: FILTROS DINÂMICOS
    # ==========================================
    st.sidebar.title("🎛️ Filtros de Investigação")
    
    # 1. Filtro de Ano
    ano_selecionado = st.sidebar.selectbox(
        "Ano de Referência:",
        options=["Todos os Anos"] + filter_opts["anos"],
        index=1  # Padrão: 2023 (ou ano mais recente com ciclo completo)
    )
    anos_filtro = [ano_selecionado] if ano_selecionado != "Todos os Anos" else None
    
    # 2. Filtro de Etapa de Ensino
    etapa_selecionada = st.sidebar.selectbox(
        "Etapa de Ensino:",
        options=["Todas as Etapas"] + filter_opts["etapas"],
        index=2  # Padrão: Anos Finais (onde se concentra a maior parte dos colégios cívico-militares)
    )
    etapas_filtro = [etapa_selecionada] if etapa_selecionada != "Todas as Etapas" else None
    
    # 3. Filtro de Rede de Ensino
    redes_selecionadas = st.sidebar.multiselect(
        "Rede de Ensino:",
        options=filter_opts["redes"],
        default=filter_opts["redes"]
    )
    
    # 4. Filtro de Município
    municipios_selecionados = st.sidebar.multiselect(
        "Municípios (deixe em branco para todos):",
        options=filter_opts["municipios"],
        default=[]
    )
    
    # 5. Filtro de Tipo de Gestão
    tipo_gestao = st.sidebar.radio(
        "Grupo de Gestão:",
        options=["Todas", "Cívico-Militar", "Não Cívico-Militar"],
        index=0,
        horizontal=True
    )
    
    # 6. Busca textual por escola / ID
    busca_escola = st.sidebar.text_input(
        "Buscar escola por nome ou código INEP:",
        placeholder="Ex: Alberto Krause, 41122801..."
    )
    
    # Aplicação dos filtros
    df_filtrado = apply_filters(
        df_raw,
        anos=anos_filtro,
        etapas=etapas_filtro,
        redes=redes_selecionadas,
        municipios=municipios_selecionados if municipios_selecionados else None,
        tipo_gestao=tipo_gestao,
        search_query=busca_escola
    )
    
    # Resumo da Amostra na Sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("##### 📊 Amostra Filtrada")
    total_linhas = len(df_filtrado)
    total_cm = (df_filtrado["TIPO_GESTAO"] == "Cívico-Militar").sum()
    total_ncm = (df_filtrado["TIPO_GESTAO"] == "Não Cívico-Militar").sum()
    
    st.sidebar.write(f"Total de registros: **{total_linhas:,}**")
    st.sidebar.write(f"• Cívico-Militares: **{total_cm:,}**")
    st.sidebar.write(f"• Não Cívico-Militares: **{total_ncm:,}**")
    
    if total_linhas == 0:
        st.warning("Nenhum dado encontrado para a combinação de filtros selecionada. Ajuste os filtros na barra lateral.")
        st.stop()
        
    # ==========================================
    # NAVEGAÇÃO PRINCIPAL (ABAS)
    # ==========================================
    nav_tab1, nav_tab2, nav_tab3, nav_tab4, nav_tab5, nav_tab6 = st.tabs([
        "🎯 SAEB (Principal)",
        "📈 Séries Históricas",
        "📊 IDEB & Rendimento",
        "🗺️ Comparativo Municipal",
        "🔎 Explorador & Microdados",
        "📖 Metodologia & Transparência"
    ])
    
    with nav_tab1:
        render_saeb_view(df_filtrado)
        
    with nav_tab2:
        # Na evolução temporal, passamos o dataframe sem o filtro de ano único se o usuário filtrou um único ano
        # para que ele possa ver a série completa da etapa/municípios selecionados
        df_temporal = apply_filters(
            df_raw,
            anos=None,
            etapas=etapas_filtro,
            redes=redes_selecionadas,
            municipios=municipios_selecionados if municipios_selecionados else None,
            tipo_gestao=tipo_gestao,
            search_query=busca_escola
        )
        render_temporal_view(df_temporal)
        
    with nav_tab3:
        render_complementary_view(df_filtrado)
        
    with nav_tab4:
        render_geo_view(df_filtrado)
        
    with nav_tab5:
        render_explorer_view(df_filtrado)
        
    with nav_tab6:
        render_methodology_view()

if __name__ == "__main__":
    main()
