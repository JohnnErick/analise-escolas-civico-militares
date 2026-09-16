import streamlit as st
import pandas as pd
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
            
            # Exportação CSV
            csv_data = df_filtrado[colunas_selecionadas].to_csv(index=False, sep=";", encoding="utf-8-sig")
            st.download_button(
                label="📥 Baixar Dados Filtrados em CSV (Excel)",
                data=csv_data,
                file_name="analise_escolas_filtrado.csv",
                mime="text/csv"
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
            
            st.markdown(f"#### Histórico de Desempenho: **{info_escola['NO_ESCOLA']}**")
            
            # Histórico das notas em tabela
            tabela_historico = escola_df[[
                "ANO", "ETAPA", "SAEB_PORTUGUES", "SAEB_MATEMATICA",
                "SAEB_NOTA_MEDIA", "IDEB_OBSERVADO", "IDEB_PROJECAO", "TAXA_APROVACAO"
            ]].copy()
            
            st.dataframe(
                tabela_historico.style.format({
                    "SAEB_PORTUGUES": "{:.1f}",
                    "SAEB_MATEMATICA": "{:.1f}",
                    "SAEB_NOTA_MEDIA": "{:.2f}",
                    "IDEB_OBSERVADO": "{:.2f}",
                    "IDEB_PROJECAO": "{:.2f}",
                    "TAXA_APROVACAO": "{:.1f}%"
                }),
                use_container_width=True,
                hide_index=True
            )
            
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
