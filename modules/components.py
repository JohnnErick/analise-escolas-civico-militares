import streamlit as st
import pandas as pd
import numpy as np

def render_header():
    st.title("🏛️ Painel de Análise: Escolas Cívico-Militares")
    st.markdown(
        """
        **Ambiente de Exploração e Investigação Educacional**  
        *Dados Oficiais do INEP/MEC — Estado do Paraná*
        """
    )
    
def render_investigation_banner():
    st.info(
        """
        ℹ️ **Princípio de Investigação Jornalística e Neutralidade Analítica:**  
        Este painel foi desenvolvido para propiciar a exploração transparente dos microdados educacionais. 
        Não se assume previamente superioridade ou inferioridade de nenhum modelo pedagógico/administrativo. 
        As métricas apresentadas devem ser analisadas considerando o contexto socioeconômico, histórico escolar e filtros aplicados.
        """,
        icon="🔍"
    )

def render_kpi_cards(df: pd.DataFrame, metric_col: str, metric_title: str, format_str="{:.1f}"):
    df_cm = df[df["TIPO_GESTAO"] == "Cívico-Militar"][metric_col].dropna()
    df_ncm = df[df["TIPO_GESTAO"] == "Não Cívico-Militar"][metric_col].dropna()
    
    n_cm = len(df_cm)
    n_ncm = len(df_ncm)
    
    mean_cm = df_cm.mean() if n_cm > 0 else np.nan
    mean_ncm = df_ncm.mean() if n_ncm > 0 else np.nan
    
    med_cm = df_cm.median() if n_cm > 0 else np.nan
    med_ncm = df_ncm.median() if n_ncm > 0 else np.nan
    
    diff_mean = (mean_cm - mean_ncm) if (pd.notna(mean_cm) and pd.notna(mean_ncm)) else np.nan
    diff_med = (med_cm - med_ncm) if (pd.notna(med_cm) and pd.notna(med_ncm)) else np.nan
    
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.metric(
            label=f"Cívico-Militar — Média ({metric_title})",
            value=format_str.format(mean_cm) if pd.notna(mean_cm) else "Sem dados",
            help=f"Mediana: {format_str.format(med_cm) if pd.notna(med_cm) else 'N/A'}"
        )
        st.caption(f"Amostra: **{n_cm:,}** escolas avaliadas")
        
    with c2:
        st.metric(
            label=f"Não Cívico-Militar — Média ({metric_title})",
            value=format_str.format(mean_ncm) if pd.notna(mean_ncm) else "Sem dados",
            help=f"Mediana: {format_str.format(med_ncm) if pd.notna(med_ncm) else 'N/A'}"
        )
        st.caption(f"Amostra: **{n_ncm:,}** escolas avaliadas")
        
    with c3:
        delta_str = f"{diff_mean:+.2f}" if pd.notna(diff_mean) else "-"
        st.metric(
            label="Diferença Absoluta (Médias)",
            value=delta_str,
            delta=delta_str if pd.notna(diff_mean) else None,
            delta_color="off"  # Mantém cor neutra para não enviesar bom/ruim
        )
        st.caption("Diferença simples: CM menos Não-CM")
        
    with c4:
        delta_med_str = f"{diff_med:+.2f}" if pd.notna(diff_med) else "-"
        st.metric(
            label="Diferença Absoluta (Medianas)",
            value=delta_med_str,
            delta=delta_med_str if pd.notna(diff_med) else None,
            delta_color="off"
        )
        st.caption("Resistente a valores extremos/outliers")

def render_stats_table(df: pd.DataFrame, metric_col: str, metric_name: str):
    df_valid = df.dropna(subset=[metric_col, "TIPO_GESTAO"])
    if df_valid.empty:
        st.warning("Não há dados suficientes para a tabela descritiva com os filtros atuais.")
        return
        
    stats = df_valid.groupby("TIPO_GESTAO")[metric_col].agg(
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
        "Tipo de Gestão", "Nº Escolas", "Média", "Desvio Padrão",
        "Mínimo", "1º Quartil (25%)", "Mediana (50%)", "3º Quartil (75%)", "Máximo"
    ]
    
    st.markdown(f"##### Sumário Estatístico Completo — {metric_name}")
    st.dataframe(
        stats.style.format({
            "Nº Escolas": "{:,}",
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
