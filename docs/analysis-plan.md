# Plano Analítico de Investigação Estatística (Pré-Registro)

> **Investigação**: Colégios Cívico-Militares do Paraná  
> **Documento**: Plano de Desenho Estatístico e Pré-Registro Metodológico  
> **Data**: 2026-09-18  
> **Status**: Proposto e Validado Empiricamente  

---

## 1. Pergunta de Pesquisa Principal

> **Pergunta Principal**:
> *As escolas da rede pública estadual do Paraná que foram selecionadas e adotaram o modelo cívico-militar (CCM) a partir de 2024 já apresentavam trajetórias prévias e características educacionais diferenciadas em relação às escolas que permaneceram no modelo regular tradicional?*

Esta pergunta ancora formalmente a investigação na realidade factual dos dados disponíveis (cujo horizonte recente de SAEB, IDEB e Censo Escolar vai até 2023, período anterior à implantação do modelo para o lote principal de 2024).

---

## 2. Perguntas Secundárias

1. **Seleção e Linha de Base (Baseline)**: Qual era o perfil educacional pré-intervenção das escolas destinadas ao modelo CCM em comparação às demais escolas estaduais regulares em termos de proficiência (SAEB Língua Portuguesa e Matemática), fluxo (taxas de aprovação e abandono) e complexidade?
2. **Tendências Prévias (Parallel Trends Check)**: Antes da intervenção de 2024, as escolas do grupo CCM e as escolas regulares seguiam trajetórias paralelas de desempenho e fluxo, ou já havia divergência estrutural prévia?
3. **Grupo de Consulta sem Homologação (Quasi-Experimento)**: As 62 escolas cujas comunidades escolares foram consultadas pelo governo mas rejeitaram o modelo (ou não alcançaram quórum) diferem em sua trajetória prévia das 106 escolas que aprovaram a adesão?
4. **Protocolo Ex-Ante para Dados Futuros (SAEB 2025 / Censo 2024)**: Quando forem divulgados os microdados oficiais pós-intervenção, qual é o estimador quase-experimental pré-especificado para quantificar o efeito causal do modelo sobre proficiência e fluxo escolar?

---

## 3. População Elegível e Amostras Analíticas

- **População Original Auditada**: 201 escolas com eventos documentais em Diários Oficiais e Editais da SEED/PR.
- **Universo Potencial de Controle**: Aproximadamente 1.800 a 1.870 escolas públicas regulares da rede estadual do Paraná presentes nos cadastros oficiais do INEP (SAEB e Censo Escolar).
- **Recorte por Etapa de Ensino**:
  - **Amostra Principal**: Anos Finais do Ensino Fundamental (6º ao 9º ano) — etapa central com 197 escolas CCM ofertantes e maior cobertura histórica contínua de SAEB e IDEB.
  - **Amostra Secundária**: Ensino Médio — etapa com 160 escolas CCM ofertantes, avaliada de forma estratificada devido à universalização censitária do SAEB ter ocorrido somente a partir de 2017.
  - **Amostra Excluída da Análise Principal**: Anos Iniciais do Ensino Fundamental (1º ao 5º ano), presente em apenas 21 escolas residuais na rede estadual, sem participantes nas edições recentes do SAEB na rede estadual.

---

## 4. Unidade de Análise

A unidade de observação econométrica é definida estritamente como:

$$\text{Escola } (i) \times \text{Ano Letivo } (t) \times \text{Etapa de Ensino } (e)$$

Não são misturadas etapas distintas em uma mesma observação. Cada etapa possui dinâmicas curriculares, escalas de proficiência e taxas de aprovação próprias.

---

## 5. Definição do Grupo de Tratamento

O status de tratamento é extraído exclusivamente da base auditada e congelada [`historico_ccm_por_ano.csv`](file:///home/johnnericks/Workspace/analise-escolas/data/processed/historico_ccm_por_ano.csv):
- **Tratamento Principal (Lote 2024)**: As **106 escolas** cuja homologação formal de início foi fixada a partir de **01/01/2024** (Editais nº 107/2023, 121/2023 e 128/2023).
- **Lote Futuro 2026 (33 escolas)**: Mantidas fora do grupo de tratamento atual, pois sua implantação só ocorrerá em 2026. Servem como grupo de validação pré-intervenção.

---

## 6. Definição dos Grupos de Controle

Para garantir robustez analítica contra viés de seleção, são estruturados dois grupos de comparação:
1. **Controle Regular Geral Pareado (Regular Matched Control)**: Amostra pareada extraída do universo de mais de 1.800 colégios da rede estadual que permaneceram sob gestão civil tradicional, selecionados via *Propensity Score Matching* com base em indicadores prévios (desempenho SAEB 2019, aprovação e abandono 2017–2019).
2. **Controle Quase-Experimental ("Consultadas mas Rejeitadas")**: As **62 escolas** cujas comunidades escolares foram selecionadas pela SEED/PR para consulta pública, mas rejeitaram o modelo ou não atingiram quórum de aprovação. Este grupo compartilha os critérios de elegibilidade institucional utilizados pelo governo, constituindo um contrafactual natural valioso.

---

## 7. Tratamento do Status `INDETERMINADO`

- As **62 escolas** com `ano_inicio_ccm = INDETERMINADO` **não são convertidas automaticamente em tratamento nem em controle geral**.
- Elas são isoladas como uma categoria analítica específica (`CONSULTA_REJEITADA`), permitindo estimar a diferença entre comunidades escolares que aceitaram e comunidades que recusaram o modelo militar.

---

## 8. Definição dos Períodos Pré e Pós-Tratamento

Dada a cronologia da política e a disponibilidade de dados oficiais divulgados pelo INEP até a presente data:
- **Período Pré-Tratamento (Baseline)**:
  - **SAEB / IDEB**: Edições de **2017, 2019, 2021 e 2023**;
  - **Rendimento Escolar (Censo)**: Anos letivos de **2017 a 2023**.
- **Ano de Transição / Implantação**: **2024** (início do modelo cívico-militar nas 106 escolas).
- **Período Pós-Tratamento**:
  - **Rendimento Escolar**: Censo Escolar 2024 (quando os dados de situação do aluno forem publicados pelo INEP);
  - **SAEB / IDEB**: Edição do SAEB 2025 (com divulgação dos microdados prevista pelo INEP para meados de 2026).

> **Aviso Crítico de Interpretação**:
> Como os dados do SAEB 2023 foram coletados em outubro/novembro de 2023, eles refletem o desempenho da escola **enquanto colégio regular estadual**. Nenhuma diferença observada até 2023 pode ser atribuída à gestão cívico-militar.

---

## 9. Hierarquia de Indicadores de Resultado (Outcomes)

1. **Indicadores Primários (Proficiência Cognitiva Padronizada)**:
   - `saeb_matematica`: Proficiência média padronizada da escola na escala TRI Saeb (0 a 500);
   - `saeb_portugues`: Proficiência média padronizada da escola na escala TRI Saeb (0 a 500).
2. **Indicadores Secundários (Fluxo e Rendimento Escolar)**:
   - `taxa_aprovacao`: Proporção de alunos aprovados ao final do ano letivo (0,0% a 100,0%);
   - `taxa_reprovacao`: Proporção de alunos reprovados na série (0,0% a 100,0%);
   - `taxa_abandono`: Proporção de alunos evadidos durante o ano letivo (0,0% a 100,0%).
3. **Indicador Sintético Complementar**:
   - `ideb_observado`: Índice sintético calculado pelo INEP ($IDEB = N \times P$). Analisado separadamente para evitar dupla contagem.

---

## 10. Covariáveis de Controle e Pareamento

As covariáveis são medidas **estritamente no período pré-tratamento** (2017 a 2019 / 2021) para não sofrerem contaminação pós-intervenção:
- **Desempenho Educacional Prévio**: Proficiência em Matemática e Português em 2017 e 2019;
- **Fluxo Escolar Prévio**: Taxa média histórica de aprovação e abandono pré-pandemia (2017 a 2019);
- **Localização Geográfica**: Macrorregião / Município / Núcleo Regional de Educação (NRE);
- **Porte Escolar**: Tamanho do corpo discente apurado no Censo Escolar;
- **Vulnerabilidade Institucional**: Indicador de distorção idade-série prévio.

---

## 11. Métodos Estatísticos Selecionados

### Fase 1 (Executável Imediatamente com os Dados Disponíveis)
1. **Estatística Descritiva Longitudinal e Testes de Médias de Linha de Base**:
   - Comparação das trajetórias históricas 2005–2023 entre grupo CCM 2024 e rede regular;
   - Decomposição das diferenças pré-existentes na linha de base.
2. **Modelo de Seleção / Escore de Propensão (Propensity Score Estimation)**:
   - Regressão logística estimando a probabilidade de uma escola ser selecionada para o modelo CCM em função de suas métricas prévias de desempenho e fluxo;
   - Verificação de suporte comum e identificação de pares equivalentes na rede regular.
3. **Teste de Tendências Paralelas Placebo (Placebo DiD)**:
   - Estimação de um modelo DiD falso utilizando 2017/2019 como pré e 2021/2023 como pós, atestando formalmente se as trajetórias divergiam antes da adoção da política.

### Fase 2 (Protocolo Pré-Registrado para Execução Pós-2024/2025)
1. **Diferenças-em-Diferenças com Pareamento por Escore de Propensão (PSM-DiD)**:
   - Estimador duplamente robusto (Doubly Robust DiD) comparando a variação pré $\to$ pós das escolas CCM 2024 contra seus pares regulares idênticos na linha de base.

---

## 12. Hipóteses de Identificação Causal

Para que qualquer resultado futuro seja interpretado como efeito do modelo CCM, as seguintes hipóteses devem ser satisfeitas:
1. **Tendências Paralelas**: Na ausência do modelo CCM, a trajetória média das escolas CCM teria evoluído de forma paralela à do grupo de controle;
2. **SUTVA (Stable Unit Treatment Value Assumption)**: A adoção do modelo em uma escola não afeta o desempenho das escolas vizinhas não militarizadas (ausência de transbordamento / spillover massivo de alunos);
3. **Invariância de Composição Discente**: A migração de estudantes (transferências voluntárias ou evasão seletiva após a militarização) não pode alterar drasticamente o perfil socioeconômico da escola tratada.

---

## 13. Testes de Robustez Pré-Especificados

1. **Placebo Temporal**: Testado no período 2017 $\to$ 2023 (coeficiente deve ser estatisticamente nulo);
2. **Controle Alternativo**: Comparação contra as 62 escolas consultadas que rejeitaram o modelo vs. comparação contra os controles regulares gerais;
3. **Estratificação por Etapa**: Estimação separada para Anos Finais e Ensino Médio;
4. **Sensibilidade ao Pareamento**: Variação do algoritmo de matching (vizinho mais próximo 1:1, kernel matching e raio);
5. **Corte de Casos Extremos (Trimming)**: Exclusão de observações com propensity score nos percentis extremos (< 1% e > 99%).

---

## 14. Tratamento de Valores Ausentes e Não-Divulgação (`ND`)

- Valores ausentes permanecem como `NaN` numérico com rotulagem explícita no campo de status;
- **Zero Imputação Arbitrária**: Nenhuma nota ou taxa ausente é substituída por zero ou média amostral;
- **Análise de Sensibilidade de Atrição**: Avaliação formal se escolas com `ND` no SAEB diferem sistematicamente das escolas com notas divulgadas, prevenindo viés de seleção por presença discente na prova.

---

## 15. Critérios de Exclusão

- Escolas sem oferta da respectiva etapa de ensino;
- Escolas com código INEP ambíguo isolado como erro material (`41146093`);
- Escolas recém-criadas sem histórico anterior (`41167090` para a análise pré-2024);
- Escolas privadas ou municipais que não integram a rede estadual.

---

## 16. Limitações Metodológicas Declaradas

1. **Inexistência de Dados Pós-Tratamento do SAEB até o Momento**: O SAEB mais recente é 2023. Não é metodologicamente viável inferir impacto causal sobre proficiência antes da divulgação do SAEB 2025;
2. **Possível Efeito de Autosseleção de Alunos**: A exigência de regras militares pode provocar a saída de alunos com maior risco de evasão ou a atração de famílias mais engajadas, o que altera a composição discente independentemente da qualidade pedagógica da escola;
3. **Ausência de Microdados de Renda Familiar por Aluno no Nível Escola**: O controle socioeconômico depende do Indicador de Nível Socioeconômico (INSE) do INEP.

---

## 17. Resultados que NÃO Poderão ser Interpretados Causalmente

- **Diferenças de médias brutas em 2021 ou 2023**: Representam diferenças pré-existentes de linha de base entre as escolas, não o efeito da política;
- **Comparações sem pareamento prévio**: Não isolam o efeito do modelo da seleção geográfica e socioeconômica das escolas escolhidas pelo governo;
- **Variações no IDEB desacompanhadas de análise de proficiência**: Podem decorrer exclusivamente de alterações nas taxas de aprovação administrativa sem ganho real de aprendizado.
