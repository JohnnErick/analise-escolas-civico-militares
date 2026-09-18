import streamlit as st
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PROCESSED_DIR = DATA_DIR / "processed"

def render_transparency_view():
    st.header("💾 Dados Abertos, Fontes Oficiais & Transparência")
    st.markdown(
        """
        Em conformidade com o princípio de reprodutibilidade e transparência da investigação jornalística, 
        todas as bases de dados auditadas e processadas estão descritas abaixo e disponíveis para download público em formato CSV.
        """
    )
    
    # Metadados de versão e auditoria
    with st.container(border=True):
        st.markdown("### ℹ️ Metadados de Atualização")
        c1, c2, c3 = st.columns(3)
        c1.metric("Data da Última Auditoria", "18/09/2026")
        c2.metric("Período Histórico Coberto", "2005 a 2026")
        c3.metric("Status da Base", "Auditada e Homologada")
        st.caption("Versão de congelamento: `v1.2-audit-final`. Não há exposição de dados pessoais sensíveis em nenhuma tabela.")

    st.markdown("---")

    # ==========================================
    # 1. FONTES OFICIAIS CONSULTADAS
    # ==========================================
    st.markdown("### 🏛️ Fontes Primárias e Rastreabilidade Documental")
    st.markdown(
        """
        Os dados foram extraídos e reconciliados a partir das seguintes fontes oficiais públicas:
        
        1. **Diário Oficial Executivo do Estado do Paraná (DIOE/PR)**:
           - Editais nº 107/2023, 121/2023 e 128/2023 — GS/SEED (Consultas e homologações do lote de 2024);
           - Edital nº 136/2025 — GS/SEED (Consultas e homologações do lote de 2026);
           - Portarias de designação e cessação de servidores militares e civis da SEED-PR.
        2. **Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP / MEC)**:
           - Microdados e Resultados Consolidados do Sistema de Avaliação da Educação Básica (SAEB 2005 a 2023);
           - Microdados de Rendimento Escolar do Censo Escolar da Educação Básica (2017 a 2023);
           - Planilhas Oficiais de Divulgação do IDEB por Escola (2005 a 2023).
        3. **Secretaria de Estado da Educação do Paraná (SEED-PR)**:
           - Relação oficial georreferenciada de Colégios Cívico-Militares (arquivo KML e listagens oficiais).
        4. **Instituto Brasileiro de Geografia e Estatística (IBGE)**:
           - Malha municipal e coordenadas oficiais dos centróides dos 399 municípios do Paraná.
        """
    )

    st.markdown("---")

    # ==========================================
    # 2. CATÁLOGO DE BASES DISPONÍVEIS PARA DOWNLOAD
    # ==========================================
    st.markdown("### 📥 Bases Disponíveis para Download (CSV)")
    st.write("Clique nos botões abaixo para baixar as bases processadas utilizadas pelo painel:")
    
    bases_info = [
        {
            "nome": "Histórico CCM por Ano",
            "arquivo": "historico_ccm_por_ano.csv",
            "descricao": "Matriz temporal anualizada (201 escolas x 7 anos 2020-2026) com status formal (SIM, NAO, INDETERMINADO), evidências e ano de início.",
            "linhas": "1.407 registros"
        },
        {
            "nome": "Eventos Documentais e Editais CCM",
            "arquivo": "historico_ccm_eventos.csv",
            "descricao": "Cronologia auditada com os 384 atos oficiais, editais, datas, páginas no Diário Oficial e evidências de homologação/rejeição.",
            "linhas": "384 registros"
        },
        {
            "nome": "Cadastro Unificado de Escolas do Paraná",
            "arquivo": "escolas_cadastro.csv",
            "descricao": "Cadastro completo das 5.966 escolas com código INEP, município, NRE, dependência administrativa, rede, coordenadas e status.",
            "linhas": "5.966 escolas"
        },
        {
            "nome": "Série Histórica SAEB (Língua Portuguesa e Matemática)",
            "arquivo": "saeb/saeb_escolas_parana_tidy.csv",
            "descricao": "Microdados organizados do SAEB por escola, etapa e ano (2005 a 2023), contendo proficiências, nota média e status de participação.",
            "linhas": "62.871 registros"
        },
        {
            "nome": "Rendimento Escolar (Censo da Educação Básica)",
            "arquivo": "rendimento/rendimento_escolas_parana_tidy.csv",
            "descricao": "Taxas de aprovação, reprovação e abandono apuradas pelo Censo Escolar entre 2017 e 2023 por escola e etapa.",
            "linhas": "126.546 registros"
        },
        {
            "nome": "Série Histórica IDEB",
            "arquivo": "ideb/ideb_escolas_parana_tidy.csv",
            "descricao": "Resultados observados do IDEB, metas projetadas pelo MEC e componentes N e P por escola e etapa (2005 a 2023).",
            "linhas": "62.871 registros"
        },
        {
            "nome": "Base Integrada de Séries Históricas CCM",
            "arquivo": "ccm_saeb_rendimento_ideb_serie_completa.csv",
            "descricao": "Cruzamento completo das escolas CCM auditadas com todas as variáveis históricas de SAEB, Rendimento e IDEB.",
            "linhas": "5.878 registros"
        }
    ]
    
    for base in bases_info:
        file_p = PROCESSED_DIR / base["arquivo"]
        with st.container(border=True):
            col_txt, col_dl = st.columns([4, 1])
            with col_txt:
                st.markdown(f"#### 📄 **{base['nome']}**")
                st.write(base["descricao"])
                st.caption(f"Dimensão: **{base['linhas']}** • Arquivo: `{base['arquivo']}`")
            with col_dl:
                st.write("")
                st.write("")
                if file_p.exists():
                    with open(file_p, "rb") as f:
                        st.download_button(
                            label="⬇️ Baixar CSV",
                            data=f,
                            file_name=Path(base["arquivo"]).name,
                            mime="text/csv",
                            key=f"dl_{base['arquivo'].replace('/', '_')}",
                            use_container_width=True
                        )
                else:
                    st.caption("Arquivo sendo preparado")
