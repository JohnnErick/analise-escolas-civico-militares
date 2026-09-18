import streamlit as st
import pandas as pd
from pathlib import Path

def render_methodology_view():
    st.header("📖 Metodologia, Dicionário de Dados e Transparência")
    st.markdown(
        """
        Em conformidade com os princípios de transparência jornalística e rigor metodológico, 
        esta seção documenta a proveniência dos dados, critérios de classificação adotados, 
        estruturação das variáveis e eventuais limitações das bases.
        """
    )
    
    with st.expander("📁 1. Origem e Estrutura dos Arquivos de Dados", expanded=True):
        st.markdown(
            """
            - **Fontes Primárias**:
              1. **INEP / MEC**: Planilhas Oficiais de Divulgação do IDEB e SAEB para o Estado do Paraná (`planilha ref/divulgacao_pr_consolidado.xlsx`).
              2. **SEED-PR / KML Geoespacial**: Relação Oficial de Colégios Cívico-Militares do Estado do Paraná com coordenadas geográficas auditadas (`planilha ref/Colégios Cívico-Militares do Paraná.kml` e `planilha ref/escolas_civico_militares_pr-final.csv`).
              3. **IBGE**: Malha e coordenadas centróides dos 399 municípios paranaenses.
            - **Abas Contempladas na Base Consolidada**:
              1. `divulgacao_anos_iniciais`: Anos Iniciais do Ensino Fundamental (1º ao 5º ano) — 2.976 escolas.
              2. `divulgacao_anos_finais`: Anos Finais do Ensino Fundamental (6º ao 9º ano) — 1.965 escolas.
              3. `divulgacao_ensino_medio`: Ensino Médio — 1.704 escolas.
            - **Total de Escolas Únicas**: 4.941 estabelecimentos de ensino no Paraná.
            - **Período Coberto**: De **2005 a 2025** (séries bianuais para Anos Iniciais e Finais; 2017 a 2025 para Ensino Médio).
            """
        )
        
    with st.expander("🏷️ 2. Critério de Classificação: Cívico-Militar vs Não Cívico-Militar", expanded=True):
        st.markdown(
            """
            As escolas cívico-militares no Paraná foram instituídas no âmbito do Programa dos Colégios Cívico-Militares do Paraná (SEED-PR), formalizado pela Lei Estadual nº 20.338/2020 e expansões subsequentes.
            
            **Regra Documentada de Classificação:**
            1. **Mapeamento Geoespacial Multi-Critério**: Cruzamento dos 306 pontos georreferenciados do KML com as coordenadas municipais do IBGE e códigos `ID_ESCOLA` do INEP, eliminando ambiguidades e falsos positivos.
            2. **Validação por Nomenclatura Oficial**: Identificação das siglas padronizadas da SEED-PR e INEP:
               - `C E CM`: Colégio Estadual Cívico-Militar;
               - `E E CM`: Escola Estadual Cívico-Militar;
               - `E M CM` / `E C M`: Escola Municipal / Estadual Cívico-Militar;
               - `CMEF`: Colégio Estadual Cívico-Militar Ensino Fundamental;
               - `CPM`: Colégio da Polícia Militar;
               - Expressões literais: `CÍVICO-MILITAR`, `CIVICO MILITAR` ou `MILITAR`.
            3. **Filtro de Exclusão**: Foram expressamente desconsiderados os registros contendo `CMEI` ou `C M E I` (Centros Municipais de Educação Infantil), assegurando que creches e pré-escolas municipais não fossem indevidamente rotuladas.
            4. **Distribuição da Amostra por Etapa (Universo de 306 Colégios Oficiais)**:
               - **Relação Oficial SEED-PR (KML)**: **306 colégios** (100% mapeados e georreferenciados).
               - **Anos Finais (6º ao 9º)**: **322 escolas** cadastradas, das quais **315 escolas** possuem notas no SAEB 2023.
               - **Ensino Médio**: **293 escolas** cadastradas, das quais **260 escolas** possuem notas no SAEB 2023.
               - **Anos Iniciais (1º ao 5º)**: **48 escolas** cadastradas, das quais apenas **18 escolas** tinham turmas de 5º ano avaliadas no SAEB 2023 (pois esta etapa é de competência quase 100% municipal).
               - **Total de Escolas Únicas no Paraná**: **343 escolas cívico-militares únicas** com registros históricos consolidados.
            """
        )
        
    with st.expander("📊 3. Dicionário de Indicadores Educacionais", expanded=True):
        st.markdown(
            """
            | Indicador | Sigla na Base Original | Definição e Escala | Papel no Painel |
            | :--- | :--- | :--- | :--- |
            | **Proficiência SAEB Matemática** | `VL_NOTA_MATEMATICA_YYYY` | Escala contínua do SAEB (tipicamente 150 a 400 pontos). Avalia competências matemáticas. | **Indicador Principal** |
            | **Proficiência SAEB Português** | `VL_NOTA_PORTUGUES_YYYY` | Escala contínua do SAEB (tipicamente 150 a 400 pontos). Avalia leitura e interpretação de texto. | **Indicador Principal** |
            | **Nota Média Padronizada** | `VL_NOTA_MEDIA_YYYY` | Nota padronizada de 0 a 10 calculada pelo INEP a partir do SAEB ($N$ na fórmula do IDEB). | **Indicador Principal** |
            | **IDEB Observado** | `VL_OBSERVADO_YYYY` | Índice de Desenvolvimento da Educação Básica (0 a 10), calculado por $IDEB = N \\times P$. | **Indicador Complementar** |
            | **Meta do IDEB (Projeção)** | `VL_PROJECAO_YYYY` | Meta bianual calculada pelo MEC para a unidade escolar. | **Indicador Complementar** |
            | **Taxa de Aprovação Global** | `VL_APROVACAO_YYYY_SI_4` | Percentual de estudantes aprovados na média dos anos da etapa (0% a 100%). | **Indicador / Target de Comparação** |
            | **Taxas de Aprovação por Série** | `VL_APROVACAO_YYYY_1` a `_4` | Percentual de aprovação discriminado por série/ano escolar individual (ex: 6º ao 9º ano ou 1ª à 3ª série). | **Target de Comparação Detalhado** |
            | **Indicador de Rendimento ($P$)** | `VL_INDICADOR_REND_YYYY` | Fator de transição/fluxo escolar calculado pelo INEP (0 a 1). | **Indicador Complementar** |
            | **Superação da Meta** | `VL_OBSERVADO` - `VL_PROJECAO` | Desvio em relação à meta oficial projetada pelo INEP. | **Indicador Comparativo** |
            """
        )
        
    with st.expander("⚖️ 4. Metodologia de Benchmarking e Grupos de Comparação", expanded=True):
        st.markdown(
            """
            Para propiciar investigações jornalísticas e científicas equilibradas, o painel disponibiliza três targets de grupo (benchmarks):
            
            1. **Rede Estadual Regular (Não CM) — [Recomendado]**:
               - Isola apenas estabelecimentos da Rede Pública Estadual geridos pela SEED-PR que mantêm o modelo civil padrão.
               - Elimina distorções decorrentes de redes municipais (focadas nos anos iniciais) ou federais/privadas.
            2. **Não Cívico-Militar (Geral)**:
               - Conjunto agregado de todas as escolas não cívico-militares filtradas pelo usuário.
            3. **Mesmo Município (Pareamento Territorial)**:
               - Considera unicamente as escolas não cívico-militares situadas nos municípios que possuem ao menos uma escola militarizada ativa, controlando parcialmente variações socioeconômicas e geográficas locais.
            """
        )
        
    with st.expander("⚠️ 5. Tratamento de Dados Ausentes e Limitações", expanded=True):
        st.markdown(
            """
            - **Siglas e Ausências do INEP**:
              - `'-'`: Dado não calculado, etapa não ofertada ou dados não aplicáveis para a unidade escolar naquele ano;
              - `'ND'`: Não Divulgado. Ocorre quando a escola não atingiu o quórum mínimo de 80% dos estudantes matriculados presentes na avaliação do SAEB, ou menos de 10 alunos na etapa.
            - **Ausência de Reprovação e Abandono**: As planilhas oficiais de divulgação do IDEB consolidadas pelo INEP disponibilizam a **taxa de aprovação** e o **indicador de rendimento**, mas não incluem colunas de taxas diretas de reprovação e abandono. Em respeito ao princípio de fidelidade, estes dados não foram inferidos ou inventados.
            - **Não Causalidade**: A mera comparação entre médias não isola o perfil socioeconômico dos estudantes, nível de vulnerabilidade da região ou processo de seleção/transição da comunidade escolar. Análises de causalidade e impactos controlados caberão às etapas futuras de modelagem econométrica/estatística.
            """
        )
        
    with st.expander("🔗 6. Auditoria do Cruzamento das Planilhas (Exclusivo Paraná)", expanded=True):
        st.markdown(
            """
            O projeto é **estritamente voltado para o Estado do Paraná (PR)**.
            Abaixo está a auditoria do cruzamento realizado entre a relação oficial 
            das escolas cívico-militares (`Colégios Cívico-Militares do Paraná.kml`) e a base oficial do INEP (`divulgacao_pr_consolidado.xlsx`).
            """
        )
        
        map_path = Path(__file__).resolve().parent.parent / "data" / "mapeamento_escolas_civico_militares.csv"
        excel_path = Path(__file__).resolve().parent.parent / "data" / "base_parana_cruzada_completa.xlsx"
        
        if map_path.exists():
            df_map = pd.read_csv(map_path, sep=";", encoding="utf-8-sig")
            st.dataframe(
                df_map[[
                    "NOME_KML", "ID_ESCOLA", "NO_ESCOLA_INEP",
                    "NO_MUNICIPIO", "LATITUDE", "LONGITUDE", "MATCH_TYPE"
                ]],
                use_container_width=True,
                height=350
            )
            
        if excel_path.exists():
            with open(excel_path, "rb") as f:
                excel_bytes = f.read()
            st.download_button(
                label="📥 Baixar Planilha Cruzada Completa (Excel .xlsx)",
                data=excel_bytes,
                file_name="base_parana_cruzada_completa.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Planilha contendo o resumo, a lista mapeada e todas as escolas do Paraná por etapa com a coluna ESCOLA_CIVICO_MILITAR e coordenadas geográficas."
            )
