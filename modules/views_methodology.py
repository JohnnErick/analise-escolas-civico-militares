import streamlit as st

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
              1. Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP / MEC) — Planilhas Oficiais de Divulgação do IDEB e SAEB para o Estado do Paraná (`planilha ref/divulgacao_pr_consolidado.xlsx`).
              2. Relação Oficial de Colégios Cívico-Militares do Estado do Paraná (`planilha ref/Escolas civico militares.xlsx`).
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
            1. **Mapeamento Oficial**: Cruzamento determinístico e por correspondência de entidades entre a lista oficial (`Escolas civico militares.xlsx`) e os códigos de identificação `ID_ESCOLA` do INEP.
            2. **Validação por Nomenclatura Oficial**: Identificação das siglas padronizadas da SEED-PR e INEP:
               - `C E CM`: Colégio Estadual Cívico-Militar;
               - `E E CM`: Escola Estadual Cívico-Militar;
               - `E M CM` / `E C M`: Escola Municipal / Estadual Cívico-Militar;
               - `CMEF`: Colégio Estadual Cívico-Militar Ensino Fundamental;
               - `CPM`: Colégio da Polícia Militar;
               - Expressões literais: `CÍVICO-MILITAR`, `CIVICO MILITAR` ou `MILITAR`.
            3. **Filtro de Exclusão**: Foram expressamente desconsiderados os registros contendo `CMEI` ou `C M E I` (Centros Municipais de Educação Infantil), assegurando que creches e pré-escolas municipais não fossem indevidamente rotuladas.
            4. **Total de Escolas Cívico-Militares Identificadas**:
               - Anos Finais: 322 escolas;
               - Ensino Médio: 293 escolas;
               - Anos Iniciais: 48 escolas.

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
            | **Taxa de Aprovação** | `VL_APROVACAO_YYYY_SI_4` | Percentual de estudantes aprovados no ano letivo (0% a 100%). | **Indicador Complementar** |
            | **Indicador de Rendimento ($P$)** | `VL_INDICADOR_REND_YYYY` | Fator de transição/fluxo escolar calculado pelo INEP (0 a 1). | **Indicador Complementar** |
            """
        )
        
    with st.expander("⚠️ 4. Tratamento de Dados Ausentes e Limitações", expanded=True):
        st.markdown(
            """
            - **Siglas e Ausências do INEP**:
              - `'-'`: Dado não calculado, etapa não ofertada ou dados não aplicáveis para a unidade escolar naquele ano;
              - `'ND'`: Não Divulgado. Ocorre quando a escola não atingiu o quórum mínimo de 80% dos estudantes matriculados presentes na avaliação do SAEB, ou menos de 10 alunos na etapa.
            - **Ausência de Reprovação e Abandono**: As planilhas oficiais de divulgação do IDEB consolidadas pelo INEP disponibilizam a **taxa de aprovação** e o **indicador de rendimento**, mas não incluem colunas de taxas diretas de reprovação e abandono. Em respeito ao princípio de fidelidade, estes dados não foram inferidos ou inventados.
            - **Não Causalidade**: A mera comparação entre médias não isola o perfil socioeconômico dos estudantes, nível de vulnerabilidade da região ou processo de seleção/transição da comunidade escolar. Análises de causalidade e impactos controlados caberão às etapas futuras de modelagem econométrica/estatística.
            """
        )
