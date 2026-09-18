import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from modules.data_loader import load_cadastro, load_historico_ano

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
    # 3. DISTRIBUIÇÃO GEOGRÁFICA & NAVEGAÇÃO
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
            if st.button("Ir para o Mapa Interativo ➔", key="btn_goto_map", use_container_width=True):
                st.session_state["nav_tab"] = "Mapa"
                st.rerun()

        with st.container(border=True):
            st.markdown("##### 🏫 **Catálogo de Escolas**")
            st.write("Pesquise por qualquer escola ou código INEP, filtre por município ou status e acesse o raio-x detalhado.")
            if st.button("Ir para Lista de Escolas ➔", key="btn_goto_schools", use_container_width=True):
                st.session_state["nav_tab"] = "Escolas"
                st.rerun()

        with st.container(border=True):
            st.markdown("##### 📈 **Evolução & Linha de Base**")
            st.write("Examine o perfil pré-intervenção das escolas e compare com o grupo de controle regular e escolas consultadas.")
            if st.button("Ir para Análise de Evolução ➔", key="btn_goto_evolution", use_container_width=True):
                st.session_state["nav_tab"] = "Evolução"
                st.rerun()
