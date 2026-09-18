import streamlit as st

def render_methodology_view():
    st.header("📖 Metodologia, Dicionário e Rigor Científico")
    st.markdown(
        """
        Em conformidade com as melhores práticas de jornalismo de dados e pesquisa educacional, 
        esta seção documenta a proveniência dos microdados, os critérios de auditoria documental, 
        a definição dos indicadores e as limitações intrínsecas da análise.
        """
    )
    
    with st.container(border=True):
        st.markdown("### 🎯 1. Sobre a Investigação Jornalística")
        st.write(
            """
            Esta plataforma é fruto de uma investigação jornalística independente sobre a implantação, expansão 
            e trajetórias educacionais dos **Colégios Cívico-Militares (CCM)** no Estado do Paraná.
            
            O objetivo primordial é **responder com dados factuais e rastreabilidade documental**:
            - **O que aconteceu?**
            - **Onde aconteceu?**
            - **Quando aconteceu?**
            - **Quais dados e documentos oficiais sustentam cada afirmação?**
            
            O painel foi desenhado de forma estritamente neutra. **Não é uma ferramenta de propaganda, nem de classificação automática ou ranking de escolas.**
            """
        )

    st.markdown("---")

    with st.container(border=True):
        st.markdown("### 🔍 2. Identificação das Escolas e Rastreabilidade Documental")
        st.markdown(
            """
            Para eliminar homônimos, descontinuidades e ambiguidades de nomes, a chave unívoca de identificação é:
            ```text
            codigo_inep / ID_ESCOLA (8 dígitos)
            ```
            
            **O fluxo de validação seguiu quatro etapas auditadas:**
            1. **Atos Oficiais em Diário Oficial**: Leitura e extração de todos os editais da Secretaria de Estado da Educação do Paraná (SEED-PR) no Diário Oficial Executivo (DIOE).
            2. **Matching Determinístico**: Cruzamento por código INEP/MEC, município oficial e denominação cadastral.
            3. **Georreferenciamento de Alta Precisão**: Mapeamento KML oficial com 306 pontos geográficos auditados.
            4. **Matriz Histórica Temporal Anualizada**: Registro do status formal da escola para cada ano do período de 2020 a 2026.
            """
        )

    st.markdown("---")

    with st.container(border=True):
        st.markdown("### 📜 3. Histórico CCM e Matriz Temporal Anualizada")
        st.markdown(
            """
            Na matriz temporal anual (`historico_ccm_por_ano.csv`), cada escola possui um dos três status a cada ano:
            
            - **`SIM`**: A escola operava formalmente sob o modelo cívico-militar a partir da vigência fixada no ato homologatório publicado no DIOE.
            - **`NAO`**: A escola operava na rede estadual regular tradicional (por exemplo, durante o ano de realização da consulta preparatória cuja vigência foi fixada apenas para o ano seguinte).
            - **`INDETERMINADO`**: Ausência de evidência documental suficiente para determinar formalmente a situação no período.
            
            > ⚠️ **AVISO FUNDAMENTAL:**  
            > **`INDETERMINADO` não significa que a escola não seja CCM.** Significa estritamente que a documentação auditada nos autos 
            > não foi suficiente para comprovar o status formal naquele período específico (como os anos de 2020 a 2022, anteriores às consultas dos editais 
            > auditados, ou as 61 escolas onde a comunidade votou pela rejeição da militarização).
            """
        )

    st.markdown("---")

    with st.container(border=True):
        st.markdown("### 📊 4. Indicadores Educacionais")
        
        st.markdown("#### A. SAEB (Sistema de Avaliação da Educação Básica)")
        st.write(
            """
            - **Língua Portuguesa e Matemática**: Proficiências médias na escala padrão do SAEB (tipicamente de 0 a 500 pontos), calculadas via Teoria de Resposta ao Item (TRI).
            - **Nota Média Padronizada**: Métrica sintética de 0 a 10 calculada pelo INEP a partir das proficiências padronizadas (componente $N$ do IDEB).
            - **Critérios de Divulgação**: O INEP exige quórum mínimo de **80% de participação dos alunos matriculados** e no mínimo **10 alunos presentes** para que o resultado de uma escola seja divulgado.
            - **Tratamento de Ausências**: Resultados não divulgados (`ND`), não participação ou ausência de turma são representados estritamente como **dados ausentes** (`NULL` / `-`), e **nunca como zero**.
            """
        )
        
        st.markdown("#### B. Rendimento Escolar (Fluxo)")
        st.write(
            """
            - Coletado anualmente pelo Censo Escolar da Educação Básica para os anos de **2017 a 2023**.
            - Composto por:
              1. **Taxa de Aprovação (%)**: Proporção de alunos aprovados ao término do ano letivo.
              2. **Taxa de Reprovação (%)**: Proporção de alunos retidos na série.
              3. **Taxa de Abandono (%)**: Proporção de alunos evadidos durante o ano letivo.
            - A soma dos três componentes equivale a 100% dos alunos com situação final apurada na etapa.
            """
        )
        
        st.markdown("#### C. IDEB (Índice de Desenvolvimento da Educação Básica)")
        st.write(
            """
            O IDEB é um **indicador sintético** calculado pelo INEP por meio da fórmula:
            $$\\text{IDEB} = N \\times P$$
            Onde:
            - $N$: Nota média de proficiência no SAEB padronizada de 0 a 10;
            - $P$: Indicador de fluxo escolar (fator baseado no tempo médio de conclusão dos ciclos escolares).
            
            > **Atenção:** O IDEB **não é uma métrica independente**. Ele combina diretamente desempenho cognitivo e taxas de aprovação. 
            Uma elevação na taxa de aprovação eleva mecanicamente o IDEB, mesmo que a nota do SAEB permaneça inalterada.
            """
        )

    st.markdown("---")

    with st.container(border=True):
        st.markdown("### ⚠️ 5. Limitações Metodológicas Explícitas")
        st.markdown(
            """
            1. **Ausência de Dados Pós-Implantação**:  
               Para o lote principal de 106 escolas com início homologado em **2024**, os dados de SAEB disponíveis cobrem até a edição de **2023** (coletada em outubro/novembro de 2023). Portanto, todos os resultados observados até 2023 refletem a escola **enquanto colégio estadual regular civil**, servindo exclusivamente como linha de base.
            2. **Limitações de Inferência Causal**:  
               A mera observação de que escolas CCM apresentavam médias superiores ou inferiores antes de 2024 reflete o processo de seleção prévia e perfil socioeconômico da comunidade escolar, e **não qualquer relação de causa e efeito**.
            3. **Escolas Sem Divulgação no SAEB**:  
               Escolas de pequeno porte que não atingiram a taxa mínima de 80% de presença ou que não ofertavam anos finais/médio nas edições não possuem proficiências publicadas pelo INEP.
            4. **Mudanças Cadastrais e Fusões**:  
               Alterações na rede estadual ao longo do horizonte 2005–2023 são tratadas mantendo-se a integridade do código INEP histórico.
            """
        )
