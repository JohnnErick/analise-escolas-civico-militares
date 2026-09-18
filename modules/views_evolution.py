import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from modules.data_loader import (
    load_cadastro,
    load_saeb_tidy,
    load_rendimento_tidy,
    load_ideb_tidy
)

@st.cache_data(show_spinner="Preparando base analítica para linha de base...")
def build_baseline_dataset() -> pd.DataFrame:
    """
    Constrói a base analítica agregada com a classificação dos 3 grupos metodológicos:
    1. CCM 2024 (106 escolas)
    2. Consultadas não convertidas (62 escolas)
    3. Rede regular (1.816 escolas estaduais)
    """
    df_cad = load_cadastro()
    df_saeb = load_saeb_tidy()
    df_rend = load_rendimento_tidy()
    df_ideb = load_ideb_tidy()
    
    # Filtra apenas escolas da Rede Estadual para comparabilidade metodológica
    estaduais = df_cad[df_cad["dependencia_administrativa"] == "Estadual"].copy()
    
    def assign_group(row):
        st_ccm = row.get("status_ccm_atual")
        if st_ccm == "SIM":
            return "CCM 2024"
        elif st_ccm == "INDETERMINADO":
            return "Consultadas não convertidas"
        elif st_ccm == "NAO_CCM":
            return "Rede regular"
        elif st_ccm == "FUTURO_2026":
            return "CCM Futuro (2026)"
        return "Outras"
        
    estaduais["GRUPO_ANALITICO"] = estaduais.apply(assign_group, axis=1)
    
    # Base Saeb
    saeb_est = df_saeb.merge(
        estaduais[["codigo_inep", "GRUPO_ANALITICO", "municipio", "nre"]],
        left_on="ID_ESCOLA",
        right_on="codigo_inep",
        how="inner"
    )
    
    # Base Rendimento
    rend_est = df_rend.merge(
        estaduais[["codigo_inep", "GRUPO_ANALITICO", "municipio", "nre"]],
        left_on="ID_ESCOLA",
        right_on="codigo_inep",
        how="inner"
    )
    
    # Base Ideb
    ideb_est = df_ideb.merge(
        estaduais[["codigo_inep", "GRUPO_ANALITICO", "municipio", "nre"]],
        left_on="ID_ESCOLA",
        right_on="codigo_inep",
        how="inner"
    )
    
    return {
        "cad": estaduais,
        "saeb": saeb_est,
        "rend": rend_est,
        "ideb": ideb_est
    }

def render_evolution_view():
    st.header("📈 Análise Agregada: Linha de Base (Baseline Pré-Intervenção)")
    
    st.warning(
        """
        ⚠️ **Aviso Metodológico Fundamental:**  
        Os microdados educacionais oficiais disponíveis até o momento (SAEB, Censo e IDEB até 2023) 
        referem-se exclusivamente ao **período anterior à implantação do modelo cívico-militar** para o lote principal de 2024.  
        **Trata-se de dados de caracterização de linha de base (baseline) e jamais devem ser interpretados como resultado ou efeito pós-intervenção.**
        """,
        icon="⚖️"
    )
    
    data_dict = build_baseline_dataset()
    df_cad_est = data_dict["cad"]
    
    # Contagem de escolas por grupo
    grupo_counts = df_cad_est["GRUPO_ANALITICO"].value_counts()
    
    g_c1, g_c2, g_c3 = st.columns(3)
    with g_c1:
        st.metric(
            "Grupo CCM 2024",
            f"{grupo_counts.get('CCM 2024', 0)} escolas",
            help="Escolas com homologação para início em 2024."
        )
    with g_c2:
        st.metric(
            "Consultadas não convertidas",
            f"{grupo_counts.get('Consultadas não convertidas', 0)} escolas",
            help="Escolas onde a consulta pública resultou em rejeição ou sem quórum para conversão."
        )
    with g_c3:
        st.metric(
            "Rede regular estadual",
            f"{grupo_counts.get('Rede regular', 0):,} escolas",
            help="Demais escolas estaduais que mantiveram a gestão civil tradicional sem processo de consulta."
        )

    st.divider()

    # ==========================================
    # FILTROS DA LINHA DE BASE
    # ==========================================
    st.markdown("### 🎛️ Filtros para Exploração da Linha de Base")
    
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        etapa_baseline = st.selectbox(
            "Etapa de Ensino:",
            options=["Anos Finais (6º-9º)", "Ensino Médio"],
            index=0,
            help="O programa cívico-militar da SEED-PR concentra-se prioritariamente nos Anos Finais."
        )
    with f2:
        indicador_tipo = st.selectbox(
            "Dimensão do Indicador:",
            options=["SAEB (Proficiência)", "Rendimento (Fluxo)", "IDEB"],
            index=0
        )
    with f3:
        if indicador_tipo == "SAEB (Proficiência)":
            metrica_escolhida = st.selectbox(
                "Indicador:",
                options=[("SAEB_MATEMATICA", "SAEB — Matemática"), ("SAEB_PORTUGUES", "SAEB — Língua Portuguesa"), ("SAEB_NOTA_MEDIA", "Nota Média Padronizada (0-10)")],
                format_func=lambda x: x[1]
            )
            anos_disp = [2023, 2021, 2019, 2017]
        elif indicador_tipo == "Rendimento (Fluxo)":
            metrica_escolhida = st.selectbox(
                "Indicador:",
                options=[("TAXA_APROVACAO", "Taxa de Aprovação (%)"), ("TAXA_REPROVACAO", "Taxa de Reprovação (%)"), ("TAXA_ABANDONO", "Taxa de Abandono (%)")],
                format_func=lambda x: x[1]
            )
            anos_disp = [2023, 2022, 2021, 2020, 2019, 2018, 2017]
        else:
            metrica_escolhida = st.selectbox(
                "Indicador:",
                options=[("IDEB_OBSERVADO", "IDEB Observado"), ("IDEB_META", "Meta Projetada pelo MEC")],
                format_func=lambda x: x[1]
            )
            anos_disp = [2023, 2021, 2019, 2017]
            
    with f4:
        ano_baseline = st.selectbox(
            "Ano de Referência Prévia:",
            options=anos_disp,
            index=0,
            help="Edição ou ano do Censo anterior à intervenção."
        )

    col_name, label_metrica = metrica_escolhida

    # Filtrar dataframe correspondente
    if indicador_tipo == "SAEB (Proficiência)":
        df_work = data_dict["saeb"]
        df_work = df_work[(df_work["ETAPA"] == etapa_baseline) & (df_work["ANO_SAEB"] == ano_baseline)].copy()
        df_work[col_name] = pd.to_numeric(df_work[col_name], errors="coerce")
    elif indicador_tipo == "Rendimento (Fluxo)":
        df_work = data_dict["rend"]
        df_work = df_work[(df_work["ETAPA"] == etapa_baseline) & (df_work["ANO"] == ano_baseline)].copy()
        df_work[col_name] = pd.to_numeric(df_work[col_name], errors="coerce")
    else:
        df_work = data_dict["ideb"]
        df_work = df_work[(df_work["ETAPA"] == etapa_baseline) & (df_work["ANO_IDEB"] == ano_baseline)].copy()
        df_work[col_name] = pd.to_numeric(df_work[col_name], errors="coerce")

    # Filtra apenas os 3 grupos principais
    df_work = df_work[df_work["GRUPO_ANALITICO"].isin(["CCM 2024", "Consultadas não convertidas", "Rede regular"])].dropna(subset=[col_name])
    
    st.markdown("---")

    # ==========================================
    # 1. DISTRIBUIÇÃO DESCRITIVA DA LINHA DE BASE (BOXPLOT)
    # ==========================================
    st.markdown(f"#### 📊 Distribuição Pré-Intervenção: {label_metrica} ({ano_baseline} — {etapa_baseline})")
    
    grupo_colors = {
        "CCM 2024": "#1E3A8A",                   # Azul escuro sóbrio
        "Consultadas não convertidas": "#7C3AED", # Violeta sóbrio
        "Rede regular": "#475569"                # Slate neutro
    }
    
    if not df_work.empty:
        fig_box = px.box(
            df_work,
            x="GRUPO_ANALITICO",
            y=col_name,
            color="GRUPO_ANALITICO",
            color_discrete_map=grupo_colors,
            points="all",
            title=f"Distribuição Descritiva Pré-Intervenção: {label_metrica} ({ano_baseline})",
            labels={
                "GRUPO_ANALITICO": "Grupo de Análise",
                col_name: label_metrica
            },
            template="plotly_white"
        )
        
        # Adicionar marcadores de média (diamante)
        means = df_work.groupby("GRUPO_ANALITICO")[col_name].mean().reset_index()
        for _, row_m in means.iterrows():
            fig_box.add_trace(go.Scatter(
                x=[row_m["GRUPO_ANALITICO"]],
                y=[row_m[col_name]],
                mode="markers+text",
                marker=dict(symbol="diamond", size=11, color="black"),
                text=[f"Média: {row_m[col_name]:.2f}"],
                textposition="top right",
                name=f"Média ({row_m['GRUPO_ANALITICO']})",
                showlegend=False
            ))
            
        fig_box.update_layout(
            showlegend=False,
            margin=dict(l=40, r=40, t=50, b=40),
            xaxis_title="",
            yaxis_title=label_metrica
        )
        st.plotly_chart(fig_box, use_container_width=True)
    else:
        st.info("Não há observações suficientes com o indicador preenchido para os filtros selecionados.")

    # ==========================================
    # 2. TABELA ESTATÍSTICA DA LINHA DE BASE
    # ==========================================
    st.markdown("##### 📋 Sumário Estatístico Descritivo (Linha de Base)")
    if not df_work.empty:
        stats = df_work.groupby("GRUPO_ANALITICO")[col_name].agg(
            Escolas="count",
            Média="mean",
            Desvio_Padrão="std",
            Mínimo="min",
            Q1=lambda x: x.quantile(0.25),
            Mediana="median",
            Q3=lambda x: x.quantile(0.75),
            Máximo="max"
        ).reset_index()
        
        stats.columns = [
            "Grupo Analítico", "Nº Escolas Avaliadas", "Média", "Desvio Padrão",
            "Mínimo", "1º Quartil (25%)", "Mediana (50%)", "3º Quartil (75%)", "Máximo"
        ]
        
        st.dataframe(
            stats.style.format({
                "Nº Escolas Avaliadas": "{:,}",
                "Média": "{:.2f}",
                "Desvio Padrão": "{:.2f}",
                "Mínimo": "{:.2f}",
                "1º Quartil (25%)": "{:.2f}",
                "Mediana (50%)": "{:.2f}",
                "3º Quartil (75%)": "{:.2f}",
                "Máximo": "{:.2f}"
            }),
            use_container_width=True,
            hide_index=True
        )
        st.caption("ℹ️ *A diferença observada reflete as características prévias dos colégios antes da adoção do modelo, evidenciando o viés de seleção natural dos processos de adesão.*")

    st.divider()

    # ==========================================
    # 3. TRAJETÓRIA HISTÓRICA PRÉ-INTERVENÇÃO
    # ==========================================
    st.markdown(f"#### 📉 Trajetórias Médias Prévias (Teste de Tendências Paralelas Pré-Intervenção)")
    st.markdown(
        """
        Permite verificar se os três grupos já seguiam trajetórias semelhantes ou divergentes antes de 2024.
        """
    )
    
    if indicador_tipo == "SAEB (Proficiência)":
        df_traj = data_dict["saeb"]
        df_traj = df_traj[
            (df_traj["ETAPA"] == etapa_baseline) & 
            (df_traj["GRUPO_ANALITICO"].isin(["CCM 2024", "Consultadas não convertidas", "Rede regular"])) &
            (df_traj["ANO_SAEB"].isin([2017, 2019, 2021, 2023]))
        ].copy()
        ano_c = "ANO_SAEB"
    elif indicador_tipo == "Rendimento (Fluxo)":
        df_traj = data_dict["rend"]
        df_traj = df_traj[
            (df_traj["ETAPA"] == etapa_baseline) & 
            (df_traj["GRUPO_ANALITICO"].isin(["CCM 2024", "Consultadas não convertidas", "Rede regular"])) &
            (df_traj["ANO"].isin([2017, 2018, 2019, 2020, 2021, 2022, 2023]))
        ].copy()
        ano_c = "ANO"
    else:
        df_traj = data_dict["ideb"]
        df_traj = df_traj[
            (df_traj["ETAPA"] == etapa_baseline) & 
            (df_traj["GRUPO_ANALITICO"].isin(["CCM 2024", "Consultadas não convertidas", "Rede regular"])) &
            (df_traj["ANO_IDEB"].isin([2017, 2019, 2021, 2023]))
        ].copy()
        ano_c = "ANO_IDEB"
        
    df_traj[col_name] = pd.to_numeric(df_traj[col_name], errors="coerce")
    traj_agg = df_traj.dropna(subset=[col_name]).groupby([ano_c, "GRUPO_ANALITICO"])[col_name].agg(
        media="mean",
        contagem="count"
    ).reset_index()
    
    if not traj_agg.empty:
        fig_traj = px.line(
            traj_agg,
            x=ano_c,
            y="media",
            color="GRUPO_ANALITICO",
            color_discrete_map=grupo_colors,
            markers=True,
            title=f"Evolução Temporal das Médias Pré-Intervenção: {label_metrica} ({etapa_baseline})",
            labels={
                ano_c: "Ano",
                "media": f"Média — {label_metrica}",
                "GRUPO_ANALITICO": "Grupo"
            },
            template="plotly_white"
        )
        
        # Marcação vertical do início da política
        fig_traj.add_vline(
            x=2024,
            line_dash="dot",
            line_color="#475569",
            line_width=2,
            annotation_text="INÍCIO CCM 2024",
            annotation_position="top left"
        )
        
        fig_traj.update_layout(
            xaxis=dict(tickmode="linear", dtick=1 if indicador_tipo == "Rendimento (Fluxo)" else 2),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=60, b=40)
        )
        st.plotly_chart(fig_traj, use_container_width=True)
    else:
        st.info("Dados insuficientes para compor a série histórica prévia.")

    st.markdown("---")

    # ==========================================
    # 4. PREPARAÇÃO PARA ANÁLISES FUTURAS
    # ==========================================
    with st.expander("🔬 Protocolo Ex-Ante & Preparação para Análise Causal Futura"):
        st.markdown(
            """
            #### Estrutura Metodológica Pré-Registrada:
            Esta seção foi arquitetada para incorporar formalmente os dados de **pós-intervenção** assim que homologados:
            
            1. **Disponibilização do Censo Escolar 2024 (Rendimento)**:
               - Permitirá avaliar se houve mudança no padrão de retenção e evasão após a intervenção nas 106 escolas.
            2. **Disponibilização do SAEB 2025 (Previsto para meados de 2026)**:
               - Primeiro ciclo censitário completo pós-intervenção.
            3. **Métodos Pré-Especificados no Plano Analítico**:
               - **Diferenças-em-Diferenças (DiD)** com efeitos fixos de escola e ano;
               - **Propensity Score Matching (PSM)** pareando escolas CCM com unidades da rede estadual com trajetórias idênticas no período 2017–2023;
               - **Análise com Grupo Quase-Experimental**: Comparação com as 62 escolas consultadas que rejeitaram o modelo.
               
            > **Compromisso Ético:** Nenhuma dessas estimativas de impacto causal está sendo executada antecipadamente, 
            respeitando a ausência de dados empíricos divulgados pelos órgãos oficiais.
            """
        )
