import math
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from modules.data_loader import load_tidy_data

@st.cache_data(show_spinner="Consolidando catálogo de escolas do Paraná...")
def get_school_catalog(df_all: pd.DataFrame) -> pd.DataFrame:
    """
    Consolida as escolas únicas com seus dados cadastrais, etapas atendidas
    e os indicadores do ano mais recente avaliado.
    """
    # Ordena por escola e ano descendente para pegar o registro mais recente
    df_sorted = df_all.sort_values(["ID_ESCOLA", "ANO"], ascending=[True, False])
    
    # Etapas atendidas agrupadas
    etapas_map = df_all.groupby("ID_ESCOLA")["ETAPA"].unique().apply(
        lambda x: ", ".join(sorted(list(set(x))))
    ).to_dict()
    
    # Registro mais recente com métrica válida ou o último ano presente
    recent_records = df_sorted.drop_duplicates(subset=["ID_ESCOLA"]).copy()
    recent_records["ETAPAS_ATENDIDAS"] = recent_records["ID_ESCOLA"].map(etapas_map)
    
    return recent_records


def render_directory_view(df_tidy: pd.DataFrame = None):
    """
    Renderiza a visão de Catálogo e Consumo Individual de Escolas (Master-Detail).
    """
    if df_tidy is None or df_tidy.empty:
        df_tidy = load_tidy_data()
        
    catalog_df = get_school_catalog(df_tidy)
    
    # Estado da escola selecionada
    if "directory_selected_school_id" not in st.session_state:
        st.session_state["directory_selected_school_id"] = None
        
    selected_id = st.session_state["directory_selected_school_id"]
    
    if selected_id is not None:
        render_school_detail(df_tidy, catalog_df, selected_id)
    else:
        render_school_list(df_tidy, catalog_df)


def render_school_list(df_tidy: pd.DataFrame, catalog_df: pd.DataFrame):
    """
    Visão de lista do catálogo de escolas com busca rápida e filtros.
    """
    st.header("🏫 Catálogo & Diretório de Escolas do Paraná")
    st.markdown(
        """
        Navegue pela lista completa de escolas públicas do Paraná. Use a busca e os filtros 
        para localizar unidades específicas e **clique em qualquer escola** para abrir o seu raio-x completo 
        com histórico de notas, comparação municipal/estadual e gráficos evolutivos.
        """
    )
    
    # ==========================================
    # BARRA DE BUSCA E FILTROS RÁPIDOS
    # ==========================================
    c_search, c_tipo, c_mun = st.columns([3, 2, 2])
    
    with c_search:
        search_term = st.text_input(
            "🔍 Buscar escola por nome ou código INEP:",
            placeholder="Ex: Hugo Simas, 41042590...",
            key="dir_search_input"
        ).strip().lower()
        
    with c_tipo:
        gestao_opt = st.selectbox(
            "Modelo de Gestão:",
            options=["Todos", "🛡️ Cívico-Militar", "🏛️ Não Cívico-Militar"],
            index=0,
            key="dir_gestao_filter"
        )
        
    with c_mun:
        municipios_disponiveis = ["Todos os Municípios"] + sorted(catalog_df["NO_MUNICIPIO"].dropna().unique().tolist())
        municipio_opt = st.selectbox(
            "Município:",
            options=municipios_disponiveis,
            index=0,
            key="dir_mun_filter"
        )
        
    with st.expander("⚙️ Filtros Adicionais e Ordenação"):
        f1, f2, f3 = st.columns(3)
        with f1:
            etapa_filter = st.selectbox(
                "Etapa de Ensino Atendida:",
                options=["Todas as Etapas", "Anos Finais (6º-9º)", "Ensino Médio", "Anos Iniciais (1º-5º)"],
                index=0,
                key="dir_etapa_filter"
            )
        with f2:
            apenas_com_saeb = st.checkbox(
                "Apenas escolas com nota SAEB recente",
                value=False,
                key="dir_saeb_check"
            )
        with f3:
            sort_opt = st.selectbox(
                "Ordenar lista por:",
                options=[
                    "Nome da Escola (A-Z)",
                    "Município (A-Z)",
                    "Maior Nota SAEB",
                    "Menor Nota SAEB",
                    "Maior IDEB",
                    "Maior Taxa de Aprovação"
                ],
                index=0,
                key="dir_sort_opt"
            )

    # ==========================================
    # APLICAÇÃO DOS FILTROS
    # ==========================================
    df_filtered = catalog_df.copy()
    
    if search_term:
        match_nome = df_filtered["NO_ESCOLA"].astype(str).str.lower().str.contains(search_term, na=False)
        match_inep = df_filtered["ID_ESCOLA"].astype(str).str.contains(search_term, na=False)
        df_filtered = df_filtered[match_nome | match_inep]
        
    if gestao_opt == "🛡️ Cívico-Militar":
        df_filtered = df_filtered[df_filtered["TIPO_GESTAO"] == "Cívico-Militar"]
    elif gestao_opt == "🏛️ Não Cívico-Militar":
        df_filtered = df_filtered[df_filtered["TIPO_GESTAO"] == "Não Cívico-Militar"]
        
    if municipio_opt != "Todos os Municípios":
        df_filtered = df_filtered[df_filtered["NO_MUNICIPIO"] == municipio_opt]
        
    if etapa_filter != "Todas as Etapas":
        df_filtered = df_filtered[df_filtered["ETAPAS_ATENDIDAS"].astype(str).str.contains(etapa_filter, na=False)]
        
    if apenas_com_saeb:
        df_filtered = df_filtered.dropna(subset=["SAEB_NOTA_MEDIA"])
        
    # Ordenação
    if sort_opt == "Nome da Escola (A-Z)":
        df_filtered = df_filtered.sort_values("NO_ESCOLA")
    elif sort_opt == "Município (A-Z)":
        df_filtered = df_filtered.sort_values(["NO_MUNICIPIO", "NO_ESCOLA"])
    elif sort_opt == "Maior Nota SAEB":
        df_filtered = df_filtered.sort_values("SAEB_NOTA_MEDIA", ascending=False)
    elif sort_opt == "Menor Nota SAEB":
        df_filtered = df_filtered.sort_values("SAEB_NOTA_MEDIA", ascending=True)
    elif sort_opt == "Maior IDEB":
        df_filtered = df_filtered.sort_values("IDEB_OBSERVADO", ascending=False)
    elif sort_opt == "Maior Taxa de Aprovação":
        df_filtered = df_filtered.sort_values("TAXA_APROVACAO", ascending=False)
        
    total_encontrado = len(df_filtered)
    st.write(f"Exibindo **{total_encontrado:,}** escolas de um total de **{len(catalog_df):,}** unidades cadastradas no Paraná.")
    
    if total_encontrado == 0:
        st.warning("Nenhuma escola corresponde aos filtros aplicados. Tente ajustar os critérios de busca.")
        return

    # ==========================================
    # ESCOLHA DO FORMATO DE CONSUMO (CARDS OU TABELA)
    # ==========================================
    modo_lista = st.radio(
        "Formato de visualização:",
        options=["🗂️ Cards Interativos com Paginação", "📋 Tabela com Seleção Direta"],
        horizontal=True,
        key="dir_modo_view"
    )
    
    if modo_lista == "📋 Tabela com Seleção Direta":
        st.info("💡 **Dica:** Clique em qualquer linha da tabela para abrir o raio-x completo daquela escola.")
        
        cols_table = [
            "ID_ESCOLA", "NO_ESCOLA", "NO_MUNICIPIO", "TIPO_GESTAO", "REDE",
            "ANO", "SAEB_NOTA_MEDIA", "IDEB_OBSERVADO", "TAXA_APROVACAO", "ETAPAS_ATENDIDAS"
        ]
        cols_table = [c for c in cols_table if c in df_filtered.columns]
        
        df_tab_show = df_filtered[cols_table].rename(columns={
            "ID_ESCOLA": "INEP",
            "NO_ESCOLA": "Nome da Escola",
            "NO_MUNICIPIO": "Município",
            "TIPO_GESTAO": "Gestão",
            "REDE": "Rede",
            "ANO": "Ano Recente",
            "SAEB_NOTA_MEDIA": "SAEB Médio",
            "IDEB_OBSERVADO": "IDEB",
            "TAXA_APROVACAO": "Aprovação (%)",
            "ETAPAS_ATENDIDAS": "Etapas"
        })
        
        event = st.dataframe(
            df_tab_show.style.format({
                "SAEB Médio": "{:.2f}",
                "IDEB": "{:.2f}",
                "Aprovação (%)": "{:.1f}%"
            }, na_rep="-"),
            use_container_width=True,
            height=500,
            selection_mode="single-row",
            on_select="rerun",
            hide_index=True,
            key="table_school_select"
        )
        
        if event and event.selection and event.selection.rows:
            sel_row_idx = event.selection.rows[0]
            chosen_id = int(df_filtered.iloc[sel_row_idx]["ID_ESCOLA"])
            st.session_state["directory_selected_school_id"] = chosen_id
            st.rerun()

    else:
        # Modo Cards Interativos
        PAGE_SIZE = 15
        total_pages = max(1, math.ceil(total_encontrado / PAGE_SIZE))
        
        c_p1, c_p2, c_p3 = st.columns([1, 2, 1])
        with c_p2:
            page_num = st.number_input(
                f"Página (1 a {total_pages}):",
                min_value=1,
                max_value=total_pages,
                value=1,
                step=1,
                key="dir_page_input"
            )
            
        start_idx = (page_num - 1) * PAGE_SIZE
        end_idx = min(start_idx + PAGE_SIZE, total_encontrado)
        df_page = df_filtered.iloc[start_idx:end_idx]
        
        st.caption(f"Mostrando escolas de {start_idx + 1} a {end_idx} (Página {page_num} de {total_pages})")
        
        for _, row in df_page.iterrows():
            id_esc = int(row["ID_ESCOLA"])
            is_cm = row["TIPO_GESTAO"] == "Cívico-Militar"
            badge_icon = "🛡️ Cívico-Militar" if is_cm else "🏛️ Não Cívico-Militar"
            badge_color = "#1E3A8A" if is_cm else "#4B5563"
            
            with st.container(border=True):
                c_info, c_kpi, c_btn = st.columns([4, 4, 2])
                
                with c_info:
                    st.markdown(f"#### **{row['NO_ESCOLA']}**")
                    st.markdown(
                        f"`INEP: {id_esc}` • 📍 **{row['NO_MUNICIPIO']}** • Rede {row['REDE']}  \n"
                        f"**Modelo:** `{badge_icon}`  \n"
                        f"**Etapas:** *{row['ETAPAS_ATENDIDAS']}*"
                    )
                    
                with c_kpi:
                    k1, k2, k3 = st.columns(3)
                    v_saeb = row.get("SAEB_NOTA_MEDIA", np.nan)
                    v_ideb = row.get("IDEB_OBSERVADO", np.nan)
                    v_aprov = row.get("TAXA_APROVACAO", np.nan)
                    ano_rec = int(row.get("ANO", 2023)) if pd.notna(row.get("ANO")) else 2023
                    
                    with k1:
                        st.metric(
                            f"SAEB ({ano_rec})",
                            f"{v_saeb:.2f}" if pd.notna(v_saeb) else "-"
                        )
                    with k2:
                        st.metric(
                            f"IDEB ({ano_rec})",
                            f"{v_ideb:.2f}" if pd.notna(v_ideb) else "-"
                        )
                    with k3:
                        st.metric(
                            f"Aprovação",
                            f"{v_aprov:.1f}%" if pd.notna(v_aprov) else "-"
                        )
                        
                with c_btn:
                    st.write("")
                    st.write("")
                    if st.button("🔍 Ver Raio-X Completo", key=f"btn_school_{id_esc}", use_container_width=True):
                        st.session_state["directory_selected_school_id"] = id_esc
                        st.rerun()


def render_school_detail(df_tidy: pd.DataFrame, catalog_df: pd.DataFrame, id_escola: int):
    """
    Visão de Detalhes (Raio-X Completo) de uma escola individual.
    """
    escola_history = df_tidy[df_tidy["ID_ESCOLA"] == id_escola].sort_values("ANO")
    
    if escola_history.empty:
        st.error(f"Escola com INEP {id_escola} não encontrada nos dados.")
        if st.button("⬅️ Voltar ao Catálogo"):
            st.session_state["directory_selected_school_id"] = None
            st.rerun()
        return

    info_base = escola_history.iloc[-1]
    nome_escola = info_base["NO_ESCOLA"]
    municipio = info_base["NO_MUNICIPIO"]
    tipo_gestao = info_base["TIPO_GESTAO"]
    is_cm = tipo_gestao == "Cívico-Militar"
    ano_recente = escola_history["ANO"].max()
    etapa_recente = escola_history[escola_history["ANO"] == ano_recente]["ETAPA"].values[0] if not escola_history.empty else ""
    rec_row = escola_history[escola_history["ANO"] == ano_recente].iloc[0]

    # Botão de retorno
    c_back, c_title = st.columns([2, 8])
    with c_back:
        if st.button("⬅️ Voltar para o Catálogo", use_container_width=True):
            st.session_state["directory_selected_school_id"] = None
            st.rerun()
            
    # Cabeçalho da Escola
    st.divider()
    badge_label = "🛡️ ESCOLA CÍVICO-MILITAR" if is_cm else "🏛️ ESCOLA NÃO CÍVICO-MILITAR"
    st.markdown(f"### {nome_escola}")
    
    h1, h2, h3, h4 = st.columns(4)
    h1.metric("Código INEP", str(id_escola))
    h2.metric("Município", municipio)
    h3.metric("Classificação", badge_label)
    h4.metric("Rede de Ensino", info_base["REDE"])

    # Metadados complementares
    etapas_todas = ", ".join(sorted(escola_history["ETAPA"].unique().tolist()))
    st.caption(f"**Etapas avaliadas:** {etapas_todas} • **Dados disponíveis de:** {escola_history['ANO'].min()} a {ano_recente}")

    # ==========================================
    # 1. INDICADORES DO ANO MAIS RECENTE
    # ==========================================
    st.markdown(f"#### 📊 Indicadores Mais Recentes (Ciclo {ano_recente} — {etapa_recente})")
    
    v_media = rec_row.get("SAEB_NOTA_MEDIA", np.nan)
    v_port = rec_row.get("SAEB_PORTUGUES", np.nan)
    v_mat = rec_row.get("SAEB_MATEMATICA", np.nan)
    v_ideb = rec_row.get("IDEB_OBSERVADO", np.nan)
    v_proj = rec_row.get("IDEB_PROJECAO", np.nan)
    v_aprov = rec_row.get("TAXA_APROVACAO", np.nan)
    v_nao_aprov = (100.0 - v_aprov) if pd.notna(v_aprov) else np.nan
    
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    with k1:
        st.metric("Nota Média SAEB", f"{v_media:.2f}" if pd.notna(v_media) else "Sem nota")
    with k2:
        st.metric("Língua Portuguesa", f"{v_port:.1f}" if pd.notna(v_port) else "-")
    with k3:
        st.metric("Matemática", f"{v_mat:.1f}" if pd.notna(v_mat) else "-")
    with k4:
        delta_meta = (v_ideb - v_proj) if (pd.notna(v_ideb) and pd.notna(v_proj)) else None
        d_meta_str = f"{delta_meta:+.2f} vs meta" if delta_meta is not None else None
        st.metric("IDEB Observado", f"{v_ideb:.2f}" if pd.notna(v_ideb) else "-", delta=d_meta_str)
    with k5:
        st.metric("Taxa de Aprovação", f"{v_aprov:.1f}%" if pd.notna(v_aprov) else "-")
    with k6:
        st.metric("Não-Aprovação", f"{v_nao_aprov:.1f}%" if pd.notna(v_nao_aprov) else "-", help="Soma de reprovação e abandono (100% - Aprovação)")

    # ==========================================
    # 2. COMPARATIVO CONTEXTUAL (ESCOLA VS MUNICÍPIO VS ESTADO)
    # ==========================================
    st.markdown(f"#### 📍 Comparativo Territorial ({ano_recente} — {etapa_recente})")
    df_mun_peer = df_tidy[(df_tidy["NO_MUNICIPIO"] == municipio) & (df_tidy["ETAPA"] == etapa_recente) & (df_tidy["ANO"] == ano_recente)]
    df_est_peer = df_tidy[(df_tidy["ETAPA"] == etapa_recente) & (df_tidy["ANO"] == ano_recente)]
    
    m_mun_saeb = df_mun_peer["SAEB_NOTA_MEDIA"].mean() if not df_mun_peer.empty else np.nan
    m_est_saeb = df_est_peer["SAEB_NOTA_MEDIA"].mean() if not df_est_peer.empty else np.nan
    diff_mun_saeb = (v_media - m_mun_saeb) if (pd.notna(v_media) and pd.notna(m_mun_saeb)) else np.nan
    
    m_mun_aprov = df_mun_peer["TAXA_APROVACAO"].mean() if not df_mun_peer.empty else np.nan
    m_est_aprov = df_est_peer["TAXA_APROVACAO"].mean() if not df_est_peer.empty else np.nan
    diff_mun_aprov = (v_aprov - m_mun_aprov) if (pd.notna(v_aprov) and pd.notna(m_mun_aprov)) else np.nan

    c_bench1, c_bench2 = st.columns(2)
    with c_bench1:
        st.markdown("**Comparação em Desempenho SAEB (Nota Média):**")
        b1, b2, b3 = st.columns(3)
        b1.metric("Esta Escola", f"{v_media:.2f}" if pd.notna(v_media) else "-")
        b2.metric(f"Média {municipio}", f"{m_mun_saeb:.2f}" if pd.notna(m_mun_saeb) else "-", help=f"Média das {len(df_mun_peer)} escolas da etapa no município")
        diff_saeb_str = f"{diff_mun_saeb:+.2f}" if pd.notna(diff_mun_saeb) else "-"
        b3.metric("Diferença vs Município", diff_saeb_str, delta=diff_saeb_str if pd.notna(diff_mun_saeb) else None, delta_color="off")
        
    with c_bench2:
        st.markdown("**Comparação em Fluxo Escolar (Taxa de Aprovação):**")
        b4, b5, b6 = st.columns(3)
        b4.metric("Esta Escola", f"{v_aprov:.1f}%" if pd.notna(v_aprov) else "-")
        b5.metric(f"Média {municipio}", f"{m_mun_aprov:.1f}%" if pd.notna(m_mun_aprov) else "-")
        diff_aprov_str = f"{diff_mun_aprov:+.1f}%" if pd.notna(diff_mun_aprov) else "-"
        b6.metric("Diferença vs Município", diff_aprov_str, delta=diff_aprov_str if pd.notna(diff_mun_aprov) else None, delta_color="off")

    # ==========================================
    # 3. HISTÓRICO COMPLETO EM TABELA E GRÁFICOS
    # ==========================================
    st.markdown("#### 📈 Evolução Histórica da Escola (2005 a 2023)")
    
    tab_graf, tab_tab = st.tabs(["📊 Gráficos de Tendência", "📋 Tabela Histórica Completa"])
    
    with tab_graf:
        g_c1, g_c2 = st.columns(2)
        
        with g_c1:
            # Gráfico SAEB (LP e MAT)
            df_saeb_chart = escola_history.dropna(subset=["SAEB_PORTUGUES", "SAEB_MATEMATICA"])
            if not df_saeb_chart.empty:
                df_melt = df_saeb_chart.melt(
                    id_vars=["ANO", "ETAPA"],
                    value_vars=["SAEB_PORTUGUES", "SAEB_MATEMATICA"],
                    var_name="Disciplina",
                    value_name="Proficiência"
                ).dropna(subset=["Proficiência"])
                
                df_melt["Disciplina"] = df_melt["Disciplina"].replace({
                    "SAEB_PORTUGUES": "Língua Portuguesa",
                    "SAEB_MATEMATICA": "Matemática"
                })
                
                fig_saeb = px.line(
                    df_melt,
                    x="ANO",
                    y="Proficiência",
                    color="Disciplina",
                    markers=True,
                    title=f"Evolução SAEB — {nome_escola}",
                    template="plotly_white",
                    color_discrete_map={"Língua Portuguesa": "#2563EB", "Matemática": "#059669"}
                )
                fig_saeb.update_layout(xaxis=dict(tickmode="linear", dtick=2), legend_title_text="")
                
                # Se for escola cívico-militar, demarca o marco de início do programa (2021)
                if is_cm:
                    fig_saeb.add_vline(
                        x=2021,
                        line_dash="dash",
                        line_color="#DC2626",
                        annotation_text="Início Cívico-Militar (2021)",
                        annotation_position="top left"
                    )
                st.plotly_chart(fig_saeb, use_container_width=True)
            else:
                st.info("Sem dados suficientes de proficiência SAEB para gerar o gráfico histórico.")
                
        with g_c2:
            # Gráfico IDEB Observado vs Projeção
            df_ideb_chart = escola_history.dropna(subset=["IDEB_OBSERVADO"])
            if not df_ideb_chart.empty:
                fig_ideb = go.Figure()
                fig_ideb.add_trace(go.Scatter(
                    x=df_ideb_chart["ANO"],
                    y=df_ideb_chart["IDEB_OBSERVADO"],
                    mode="lines+markers",
                    name="IDEB Observado",
                    line=dict(color="#1E3A8A", width=3),
                    marker=dict(size=8)
                ))
                if df_ideb_chart["IDEB_PROJECAO"].notna().any():
                    fig_ideb.add_trace(go.Scatter(
                        x=df_ideb_chart["ANO"],
                        y=df_ideb_chart["IDEB_PROJECAO"],
                        mode="lines+markers",
                        name="Meta Projetada",
                        line=dict(color="#F59E0B", width=2, dash="dash"),
                        marker=dict(size=6)
                    ))
                fig_ideb.update_layout(
                    title=f"IDEB Observado vs Meta Projetada — {nome_escola}",
                    template="plotly_white",
                    xaxis=dict(tickmode="linear", dtick=2),
                    legend_title_text=""
                )
                if is_cm:
                    fig_ideb.add_vline(
                        x=2021,
                        line_dash="dash",
                        line_color="#DC2626",
                        annotation_text="Início Cívico-Militar (2021)",
                        annotation_position="top left"
                    )
                st.plotly_chart(fig_ideb, use_container_width=True)
            else:
                st.info("Sem dados de IDEB Observado para gerar o gráfico.")

    with tab_tab:
        cols_hist = [
            "ANO", "ETAPA", "SAEB_PORTUGUES", "SAEB_MATEMATICA", "SAEB_NOTA_MEDIA",
            "IDEB_OBSERVADO", "IDEB_PROJECAO", "TAXA_APROVACAO"
        ]
        cols_present = [c for c in cols_hist if c in escola_history.columns]
        tab_df = escola_history[cols_present].copy()
        tab_df["TAXA_NAO_APROVACAO"] = 100.0 - tab_df["TAXA_APROVACAO"]
        
        fmt_hist = {
            "SAEB_PORTUGUES": "{:.1f}",
            "SAEB_MATEMATICA": "{:.1f}",
            "SAEB_NOTA_MEDIA": "{:.2f}",
            "IDEB_OBSERVADO": "{:.2f}",
            "IDEB_PROJECAO": "{:.2f}",
            "TAXA_APROVACAO": "{:.1f}%",
            "TAXA_NAO_APROVACAO": "{:.1f}%"
        }
        fmt_show = {c: fmt_hist[c] for c in tab_df.columns if c in fmt_hist}
        
        st.dataframe(
            tab_df.style.format(fmt_show, na_rep="-"),
            use_container_width=True,
            hide_index=True
        )
        st.caption("ℹ️ *Taxa de Não-Aprovação = 100% - Taxa de Aprovação (retenções + abandonos).*")

    # ==========================================
    # 4. OUTRAS ESCOLAS NO MESMO MUNICÍPIO
    # ==========================================
    st.divider()
    st.markdown(f"#### 🏘️ Outras Escolas no Município de **{municipio}**")
    outras_escolas = catalog_df[
        (catalog_df["NO_MUNICIPIO"] == municipio) & (catalog_df["ID_ESCOLA"] != id_escola)
    ].sort_values("NO_ESCOLA")
    
    if not outras_escolas.empty:
        st.write(f"Existem outras **{len(outras_escolas)}** escolas cadastradas em {municipio}:")
        
        # Selectbox com atalho para ir direto a outra escola do município
        opcoes_mun = outras_escolas["NO_ESCOLA"] + " (" + outras_escolas["TIPO_GESTAO"] + ") — INEP: " + outras_escolas["ID_ESCOLA"].astype(str)
        escolha_outra = st.selectbox(
            "Selecione outra escola de " + municipio + " para abrir:",
            options=["Selecione uma escola..."] + opcoes_mun.tolist(),
            key="sel_peer_school"
        )
        
        if escolha_outra != "Selecione uma escola...":
            novo_inep = int(escolha_outra.split("INEP: ")[-1])
            if st.button("Abrir esta escola", key="btn_confirm_peer"):
                st.session_state["directory_selected_school_id"] = novo_inep
                st.rerun()
    else:
        st.info(f"Esta é a única escola cadastrada no município de {municipio} na base de dados.")
