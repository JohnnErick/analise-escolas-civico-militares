import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from modules.data_loader import load_cadastro, load_historico_ano

def render_map_view():
    st.header("🗺️ Mapa Geográfico das Escolas no Paraná")
    st.markdown(
        """
        Explore a localização geográfica de todas as escolas cadastradas e audite espacialmente a 
        distribuição das unidades sob o modelo cívico-militar no território do Paraná.
        """
    )
    
    # Carregamento de dados
    df_cad = load_cadastro()
    df_hist = load_historico_ano()
    
    # ==========================================
    # BARRA DE FILTROS DO MAPA
    # ==========================================
    with st.expander("🎛️ Filtros de Navegação e Camadas do Mapa", expanded=True):
        f1, f2, f3 = st.columns(3)
        with f1:
            ano_ref = st.selectbox(
                "Ano de Referência Temporal:",
                options=[2026, 2025, 2024, 2023, 2022, 2021, 2020],
                index=2,  # Padrão: 2024 (ano de implantação do lote principal)
                help="O status documental CCM varia de acordo com o ano letivo selecionado."
            )
        with f2:
            escopo_mapa = st.selectbox(
                "Escopo de Escolas:",
                options=[
                    "Universo CCM Auditado (201 escolas)",
                    "Rede Pública Estadual (2.017 escolas)",
                    "Todas as Escolas do Paraná (5.966 estabelecimentos)"
                ],
                index=0,
                help="Selecione se deseja visualizar apenas as escolas que participaram dos editais CCM ou a rede estadual como um todo."
            )
        with f3:
            status_filter = st.selectbox(
                "Status CCM no Ano:",
                options=["Todos os Status", "SIM", "NAO", "INDETERMINADO", "NAO_CCM (Rede Regular)"],
                index=0,
                help="Filtra pelo status formal no ano de referência selecionado."
            )
            
        f4, f5, f6 = st.columns(3)
        with f4:
            # Lista de municípios ordenados
            municipios_list = ["Todos os Municípios"] + sorted(df_cad["municipio"].dropna().unique().tolist())
            mun_selected = st.selectbox(
                "Município:",
                options=municipios_list,
                index=0
            )
        with f5:
            # NREs disponíveis
            nres_valid = sorted([str(n) for n in df_cad["nre"].dropna().unique() if str(n).strip()])
            nre_selected = st.selectbox(
                "Núcleo Regional de Educação (NRE):",
                options=["Todos os NREs"] + nres_valid,
                index=0
            )
        with f6:
            # Etapa de ensino
            etapa_selected = st.selectbox(
                "Etapa de Ensino Ofertada:",
                options=["Todas as Etapas", "Anos Finais (6º-9º)", "Ensino Médio", "Anos Iniciais (1º-5º)"],
                index=0
            )
            
        f7, f8 = st.columns([2, 2])
        with f7:
            ano_inicio_filter = st.selectbox(
                "Ano de Início CCM Homologado:",
                options=["Todos", "2024", "2026", "INDETERMINADO", "Não se aplica (Regular)"],
                index=0
            )
        with f8:
            apenas_coordenadas_exatas = st.checkbox(
                "Exibir apenas escolas com coordenadas exatas (KML oficial)",
                value=False,
                help="Filtra apenas as escolas cujas coordenadas foram auditadas diretamente do arquivo KML oficial da SEED-PR."
            )

    # ==========================================
    # PREPARAÇÃO E CRUZAMENTO DOS DADOS PARA O MAPA
    # ==========================================
    # Junta status do histórico no ano selecionado
    df_hist_ano = df_hist[df_hist["ano"] == ano_ref][["codigo_inep", "civico_militar", "status_historico"]].copy()
    
    df_merged = df_cad.merge(df_hist_ano, on="codigo_inep", how="left")
    
    # Preenche civico_militar para escolas que não estão no histórico (são escolas regulares)
    df_merged["status_ccm_no_ano"] = df_merged["civico_militar"].fillna("NAO_CCM")
    
    # Aplicação do escopo
    if escopo_mapa == "Universo CCM Auditado (201 escolas)":
        df_filtered = df_merged[df_merged["is_ccm"] == True].copy()
    elif escopo_mapa == "Rede Pública Estadual (2.017 escolas)":
        df_filtered = df_merged[df_merged["dependencia_administrativa"] == "Estadual"].copy()
    else:
        df_filtered = df_merged.copy()
        
    # Aplicação dos filtros
    if status_filter != "Todos os Status":
        df_filtered = df_filtered[df_filtered["status_ccm_no_ano"] == status_filter]
        
    if mun_selected != "Todos os Municípios":
        df_filtered = df_filtered[df_filtered["municipio"] == mun_selected]
        
    if nre_selected != "Todos os NREs":
        df_filtered = df_filtered[df_filtered["nre"] == nre_selected]
        
    if etapa_selected != "Todas as Etapas":
        df_filtered = df_filtered[df_filtered["etapas_ofertadas"].str.contains(etapa_selected, na=False)]
        
    if ano_inicio_filter != "Todos":
        if ano_inicio_filter == "Não se aplica (Regular)":
            df_filtered = df_filtered[df_filtered["ano_inicio_ccm"].isna()]
        else:
            df_filtered = df_filtered[df_filtered["ano_inicio_ccm"] == ano_inicio_filter]
            
    if apenas_coordenadas_exatas:
        df_filtered = df_filtered[df_filtered["tipo_coordenada"] == "EXATA_KML"]
        
    total_pontos = len(df_filtered)
    total_exatos = len(df_filtered[df_filtered["tipo_coordenada"] == "EXATA_KML"])
    total_centroide = total_pontos - total_exatos
    
    st.write(
        f"Exibindo **{total_pontos:,}** escolas no mapa para o ano **{ano_ref}** "
        f"(*{total_exatos:,} com coordenadas exatas KML* e *{total_centroide:,} no centróide municipal documentado*)."
    )
    
    if total_pontos == 0:
        st.warning("Nenhuma escola corresponde aos filtros aplicados. Tente ajustar os critérios de seleção.")
        return

    # Categorização de cores neutra
    # SIM: Azul escuro sóbrio, NAO: Slate, INDETERMINADO: Âmbar, NAO_CCM: Azul claro / Ardósia suave
    color_map = {
        "SIM": "#1E3A8A",
        "NAO": "#64748B",
        "INDETERMINADO": "#D97706",
        "NAO_CCM": "#94A3B8"
    }
    
    # Preparar labels descritivos para legenda
    df_filtered["Legenda"] = df_filtered["status_ccm_no_ano"].map({
        "SIM": "CCM (Status SIM)",
        "NAO": "Regular (Status NAO)",
        "INDETERMINADO": "Status INDETERMINADO",
        "NAO_CCM": "Rede Regular Não-Participante"
    }).fillna("Outras")
    
    legend_colors = {
        "CCM (Status SIM)": "#1E3A8A",
        "Regular (Status NAO)": "#64748B",
        "Status INDETERMINADO": "#D97706",
        "Rede Regular Não-Participante": "#94A3B8",
        "Outras": "#CBD5E1"
    }

    # ==========================================
    # RENDERIZAÇÃO DO MAPA
    # ==========================================
    map_kwargs = dict(
        data_frame=df_filtered,
        lat="latitude",
        lon="longitude",
        color="Legenda",
        color_discrete_map=legend_colors,
        hover_name="nome_escola",
        hover_data={
            "codigo_inep": True,
            "municipio": True,
            "nre": True,
            "status_ccm_no_ano": True,
            "ano_inicio_ccm": True,
            "etapas_ofertadas": True,
            "tipo_coordenada": True,
            "latitude": False,
            "longitude": False,
            "Legenda": False
        },
        zoom=6.0,
        center={"lat": -24.8, "lon": -51.5},
        opacity=0.85
    )
    
    if hasattr(px, "scatter_map"):
        fig = px.scatter_map(map_style="carto-positron", **map_kwargs)
    else:
        fig = px.scatter_mapbox(mapbox_style="carto-positron", **map_kwargs)
        
    fig.update_layout(
        margin=dict(l=5, r=5, t=10, b=5),
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # Documentação obrigatória de fonte de coordenadas
    st.caption(
        """
        ℹ️ **Fonte Oficial das Coordenadas:**  
        • **Coordenadas Exatas (`EXATA_KML`)**: As coordenadas geográficas de 306 colégios cívico-militares oficiais da SEED-PR foram validadas a partir do arquivo KML oficial do programa.  
        • **Centróides Municipais (`CENTROIDE_MUNICIPIO`)**: As escolas regulares ou municipais sem georreferenciamento cadastral individual utilizam as coordenadas oficiais do centróide municipal do IBGE. Nenhuma coordenada fictícia foi inventada.
        """
    )

    st.divider()

    # ==========================================
    # CONSULTA E SELEÇÃO DIRETA DA ESCOLA NO MAPA
    # ==========================================
    st.markdown("### 🔎 Detalhes da Escola Selecionada no Mapa")
    st.markdown("Selecione uma escola filtrada acima para inspecionar seus dados cadastrais ou acessar o relatório completo:")
    
    # Opções formatadas para o selectbox
    df_sorted_picker = df_filtered.sort_values(["municipio", "nome_escola"])
    school_options = [
        f"{row['nome_escola']} — {row['municipio']} (INEP: {row['codigo_inep']})"
        for _, row in df_sorted_picker.iterrows()
    ]
    
    c_sel, c_blank = st.columns([3, 1])
    with c_sel:
        chosen_school_label = st.selectbox(
            "Selecione uma escola do mapa:",
            options=["Selecione uma escola para ver o resumo..."] + school_options,
            index=0,
            key="map_school_picker"
        )
        
    if chosen_school_label != "Selecione uma escola para ver o resumo...":
        inep_selected = int(chosen_school_label.split("INEP: ")[-1].replace(")", ""))
        esc_info = df_filtered[df_filtered["codigo_inep"] == inep_selected].iloc[0]
        
        with st.container(border=True):
            r1, r2 = st.columns([3, 1])
            with r1:
                st.markdown(f"#### **{esc_info['nome_escola']}**")
                st.markdown(
                    f"**INEP:** `{esc_info['codigo_inep']}` • "
                    f"📍 **Município:** {esc_info['municipio']} • "
                    f"🏢 **NRE:** {esc_info.get('nre', 'Não informado')} • "
                    f"🏷️ **Rede:** {esc_info['rede_ensino']}"
                )
                
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Status CCM no Ano", str(esc_info['status_ccm_no_ano']))
                m2.metric("Ano de Início CCM", str(esc_info.get('ano_inicio_ccm', 'Não CCM')) if pd.notna(esc_info.get('ano_inicio_ccm')) else "Não CCM")
                m3.metric("Tipo de Coordenada", str(esc_info['tipo_coordenada']))
                m4.metric("Situação", str(esc_info['situacao_funcionamento']))
                
                st.caption(f"**Etapas Atendidas:** {esc_info['etapas_ofertadas']}")
                
            with r2:
                st.write("")
                st.write("")
                st.write("")
                if st.button("🔍 Ver Detalhes da Escola ➔", key=f"btn_open_detail_map_{inep_selected}", use_container_width=True):
                    st.session_state["selected_inep"] = inep_selected
                    st.query_params["escola"] = str(inep_selected)
                    st.session_state["nav_tab"] = "Escolas"
                    st.rerun()
