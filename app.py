import streamlit as st
import pandas as pd
from modules.data_loader import load_tidy_data, get_filter_options, apply_filters
from modules.components import render_header, render_investigation_banner
from modules.views_comparisons import render_comparisons_view
from modules.views_saeb import render_saeb_view
from modules.views_temporal import render_temporal_view
from modules.views_complementary import render_complementary_view
from modules.views_geo import render_geo_view
from modules.views_explorer import render_explorer_view
from modules.views_directory import render_directory_view
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
    
    # 2. Filtro de Etapa de Ensino (Organizado por relevância para o programa)
    etapas_disponiveis = ["Anos Finais (6º-9º)", "Ensino Médio", "Todas as Etapas", "Anos Iniciais (1º-5º)"]
    etapa_selecionada = st.sidebar.selectbox(
        "Etapa de Ensino:",
        options=etapas_disponiveis,
        index=0,  # Padrão: Anos Finais (foco primordial dos colégios cívico-militares)
        help="O programa estadual (SEED-PR) concentra-se nos Anos Finais do Fundamental e no Ensino Médio."
    )
    etapas_filtro = [etapa_selecionada] if etapa_selecionada != "Todas as Etapas" else None
    
    if etapa_selecionada == "Anos Iniciais (1º-5º)":
        st.sidebar.info(
            "ℹ️ **Anos Iniciais**: O programa cívico-militar da SEED-PR destina-se aos Anos Finais e Ensino Médio. "
            "Nos Anos Iniciais (geridos pelas redes municipais), apenas 18 escolas estaduais cívico-militares possuíam turmas de 5º ano avaliadas no SAEB 2023.",
            icon="💡"
        )
    
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
    st.sidebar.markdown("##### 🏛️ Universo Cívico-Militar (SEED-PR)")
    st.sidebar.caption("Relação Oficial: **306 colégios** (305 estabelecimentos ativos no PR)")
    
    total_cm = df_filtrado[df_filtrado["TIPO_GESTAO"] == "Cívico-Militar"]["ID_ESCOLA"].nunique() if not df_filtrado.empty else 0
    cm_com_saeb = df_filtrado[(df_filtrado["TIPO_GESTAO"] == "Cívico-Militar") & df_filtrado["SAEB_PORTUGUES"].notna()]["ID_ESCOLA"].nunique()
    
    st.sidebar.write(f"• Cadastradas no filtro: **{total_cm:,}** escolas")
    st.sidebar.write(f"• Com notas SAEB: **{cm_com_saeb:,}** avaliadas")
    
    st.sidebar.markdown("##### 🏫 Não Cívico-Militares")
    total_ncm = df_filtrado[df_filtrado["TIPO_GESTAO"] == "Não Cívico-Militar"]["ID_ESCOLA"].nunique() if not df_filtrado.empty else 0
    ncm_com_saeb = df_filtrado[(df_filtrado["TIPO_GESTAO"] == "Não Cívico-Militar") & df_filtrado["SAEB_PORTUGUES"].notna()]["ID_ESCOLA"].nunique()

    
    st.sidebar.write(f"• Cadastradas no filtro: **{total_ncm:,}** escolas")
    st.sidebar.write(f"• Com notas SAEB: **{ncm_com_saeb:,}** avaliadas")
    
    if len(df_filtrado) == 0:
        st.warning("Nenhum dado encontrado para a combinação de filtros selecionada. Ajuste os filtros na barra lateral.")
        st.stop()

        
    # ==========================================
    # NAVEGAÇÃO PRINCIPAL (ABAS)
    # ==========================================
    nav_tab0, nav_tab1, nav_tab2, nav_tab3, nav_tab4, nav_tab5, nav_tab6, nav_tab7 = st.tabs([
        "🏫 Catálogo de Escolas",
        "⚖️ Comparações & Targets",
        "🎯 SAEB Detalhado",
        "📋 Aprovação & Rendimento",
        "📈 Séries Históricas",
        "🗺️ Comparativo Municipal",
        "🔎 Explorador & Microdados",
        "📖 Metodologia & Transparência"
    ])
    
    with nav_tab0:
        render_directory_view(df_raw)
        
    with nav_tab1:
        render_comparisons_view(df_filtrado, df_raw)
        
    with nav_tab2:
        render_saeb_view(df_filtrado)
        
    with nav_tab3:
        render_complementary_view(df_filtrado)
        
    with nav_tab4:
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
        
    with nav_tab5:
        render_geo_view(df_filtrado)
        
    with nav_tab6:
        render_explorer_view(df_filtrado)
        
    with nav_tab7:
        render_methodology_view()

if __name__ == "__main__":
    main()
