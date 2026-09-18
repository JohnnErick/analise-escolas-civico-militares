import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from modules.data_loader import load_tidy_data

def render_explorer_view(df_filtrado: pd.DataFrame):
    st.header("🔎 Explorador de Escolas & Microdados")
    st.markdown(
        """
        Consulte e filtre individualmente as escolas da base de dados, investigue o histórico completo 
        de uma escola específica e exporte os microdados para análises adicionais.
        """
    )
    
    tab_microdados, tab_ficha = st.tabs([
        "📋 Tabela de Microdados & Exportação",
        "🏫 Ficha Individual da Escola"
    ])
    
    with tab_microdados:
        st.subheader("Microdados Filtrados")
        st.write(f"Total de registros na visualização atual: **{len(df_filtrado):,}**")
        
        # Seleção de colunas para exibição
        colunas_disponiveis = [
            "ID_ESCOLA", "NO_ESCOLA", "NO_MUNICIPIO", "REDE", "ETAPA",
            "TIPO_GESTAO", "ANO", "SAEB_PORTUGUES", "SAEB_MATEMATICA",
            "SAEB_NOTA_MEDIA", "IDEB_OBSERVADO", "IDEB_PROJECAO", "TAXA_APROVACAO"
        ]
        
        colunas_selecionadas = st.multiselect(
            "Selecione as colunas para exibição na tabela:",
            options=colunas_disponiveis,
            default=[
                "ID_ESCOLA", "NO_ESCOLA", "NO_MUNICIPIO", "ETAPA",
                "TIPO_GESTAO", "ANO", "SAEB_PORTUGUES", "SAEB_MATEMATICA",
                "IDEB_OBSERVADO", "TAXA_APROVACAO"
            ]
        )
        
        if colunas_selecionadas:
            st.dataframe(
                df_filtrado[colunas_selecionadas].sort_values(["NO_MUNICIPIO", "NO_ESCOLA"]),
                use_container_width=True,
                height=450
            )
            
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                # Exportação CSV dos dados com filtros atuais
                csv_data = df_filtrado[colunas_selecionadas].to_csv(index=False, sep=";", encoding="utf-8-sig")
                st.download_button(
                    label="📥 Baixar Visualização Filtrada em CSV",
                    data=csv_data,
                    file_name="analise_escolas_filtrado.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with col_d2:
                # Download da base completa cruzada em Excel
                from pathlib import Path
                excel_completo = Path(__file__).resolve().parent.parent / "data" / "base_parana_cruzada_completa.xlsx"
                if excel_completo.exists():
                    with open(excel_completo, "rb") as f:
                        st.download_button(
                            label="📊 Baixar Base Cruzada Completa do PR (.xlsx)",
                            data=f.read(),
                            file_name="base_parana_cruzada_completa.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            help="Arquivo Excel com abas separadas por etapa e a coluna ESCOLA_CIVICO_MILITAR.",
                            use_container_width=True
                        )
        else:
            st.warning("Selecione ao menos uma coluna para exibir.")

            
    with tab_ficha:
        st.subheader("Investigação de Unidade Escolar Individual")
        
        # Carrega base completa para permitir selecionar qualquer escola
        df_all = load_tidy_data()
        
        # Opções de escolas
        escolas_unicas = df_all[["ID_ESCOLA", "NO_ESCOLA", "NO_MUNICIPIO"]].drop_duplicates()
        escolas_unicas["LABEL"] = escolas_unicas["NO_ESCOLA"] + " — " + escolas_unicas["NO_MUNICIPIO"] + " (" + escolas_unicas["ID_ESCOLA"].astype(str) + ")"
        
        escolha = st.selectbox(
            "Digite ou selecione uma escola para investigar:",
            options=escolas_unicas["LABEL"].tolist(),
            index=0 if not escolas_unicas.empty else None
        )
        
        if escolha:
            id_selecionado = int(escolha.split(" (")[-1].replace(")", ""))
            escola_df = df_all[df_all["ID_ESCOLA"] == id_selecionado].sort_values("ANO")
            
            info_escola = escola_df.iloc[0]
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Código INEP", str(info_escola["ID_ESCOLA"]))
            c2.metric("Município", info_escola["NO_MUNICIPIO"])
            c3.metric("Rede de Ensino", info_escola["REDE"])
            c4.metric("Classificação", info_escola["TIPO_GESTAO"])
            
            # Contexto Territorial no ano mais recente
            ano_recente = escola_df["ANO"].max()
            etapa_recente = escola_df[escola_df["ANO"] == ano_recente]["ETAPA"].values[0] if not escola_df.empty else ""
            rec_row = escola_df[escola_df["ANO"] == ano_recente].iloc[0]
            
            df_mun_peer = df_all[(df_all["NO_MUNICIPIO"] == info_escola["NO_MUNICIPIO"]) & (df_all["ETAPA"] == etapa_recente) & (df_all["ANO"] == ano_recente)]
            df_est_peer = df_all[(df_all["ETAPA"] == etapa_recente) & (df_all["ANO"] == ano_recente)]
            
            st.markdown(f"##### 📍 Comparativo Local: Escola vs Município e Estado (Ano {ano_recente} — {etapa_recente})")
            
            v_saeb = rec_row.get("SAEB_NOTA_MEDIA", np.nan)
            m_mun_saeb = df_mun_peer["SAEB_NOTA_MEDIA"].mean() if not df_mun_peer.empty else np.nan
            m_est_saeb = df_est_peer["SAEB_NOTA_MEDIA"].mean() if not df_est_peer.empty else np.nan
            d_mun = (v_saeb - m_mun_saeb) if (pd.notna(v_saeb) and pd.notna(m_mun_saeb)) else np.nan
            
            v_aprov = rec_row.get("TAXA_APROVACAO", np.nan)
            m_mun_aprov = df_mun_peer["TAXA_APROVACAO"].mean() if not df_mun_peer.empty else np.nan
            
            k1, k2, k3, k4 = st.columns(4)
            with k1:
                st.metric("Nota Média SAEB", f"{v_saeb:.2f}" if pd.notna(v_saeb) else "Sem nota")
            with k2:
                st.metric(f"Média em {info_escola['NO_MUNICIPIO']}", f"{m_mun_saeb:.2f}" if pd.notna(m_mun_saeb) else "-", help=f"Média das {len(df_mun_peer)} escolas da etapa no município")
            with k3:
                d_str = f"{d_mun:+.2f}" if pd.notna(d_mun) else "-"
                st.metric("Diferença vs Município", d_str, delta=d_str if pd.notna(d_mun) else None, delta_color="off")
            with k4:
                st.metric("Média Estadual (PR)", f"{m_est_saeb:.2f}" if pd.notna(m_est_saeb) else "-")
                
            st.markdown(f"#### Histórico de Desempenho: **{info_escola['NO_ESCOLA']}**")
            
            # Histórico das notas em tabela
            tabela_historico = escola_df[[
                c for c in ["ANO", "ETAPA", "SAEB_PORTUGUES", "SAEB_MATEMATICA",
                "SAEB_NOTA_MEDIA", "IDEB_OBSERVADO", "IDEB_PROJECAO", "TAXA_APROVACAO"] if c in escola_df.columns
            ]].copy()
            
            tabela_historico["TAXA_NAO_APROVACAO"] = 100.0 - tabela_historico["TAXA_APROVACAO"]
            
            fmt_hist = {
                "SAEB_PORTUGUES": "{:.1f}",
                "SAEB_MATEMATICA": "{:.1f}",
                "SAEB_NOTA_MEDIA": "{:.2f}",
                "IDEB_OBSERVADO": "{:.2f}",
                "IDEB_PROJECAO": "{:.2f}",
                "TAXA_APROVACAO": "{:.1f}%",
                "TAXA_NAO_APROVACAO": "{:.1f}%"
            }
            fmt_show = {c: fmt_hist[c] for c in tabela_historico.columns if c in fmt_hist}
            st.dataframe(
                tabela_historico.style.format(fmt_show, na_rep="-"),
                use_container_width=True,
                hide_index=True
            )
            st.caption("ℹ️ **Taxa de Não-Aprovação:** Corresponde a 100% menos a taxa de aprovação (soma de reprovações e abandonos/evasão).")
            
            # Gráfico de evolução da escola
            if not escola_df.dropna(subset=["SAEB_PORTUGUES", "SAEB_MATEMATICA"]).empty:
                df_melt = escola_df.melt(
                    id_vars=["ANO", "ETAPA"],
                    value_vars=["SAEB_PORTUGUES", "SAEB_MATEMATICA"],
                    var_name="Disciplina",
                    value_name="Proficiência"
                ).dropna(subset=["Proficiência"])
                
                df_melt["Disciplina"] = df_melt["Disciplina"].replace({
                    "SAEB_PORTUGUES": "Língua Portuguesa",
                    "SAEB_MATEMATICA": "Matemática"
                })
                
                fig_escola = px.line(
                    df_melt,
                    x="ANO",
                    y="Proficiência",
                    color="Disciplina",
                    markers=True,
                    title=f"Evolução SAEB — {info_escola['NO_ESCOLA']}",
                    template="plotly_white"
                )
                fig_escola.update_layout(xaxis=dict(tickmode="linear", dtick=2))
                st.plotly_chart(fig_escola, use_container_width=True)
