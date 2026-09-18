# Fontes de Dados do IDEB (Índice de Desenvolvimento da Educação Básica)

> **Investigação**: Colégios Cívico-Militares do Paraná  
> **Documento**: Mapeamento das Fontes Oficiais e Metodologia do IDEB  
> **Data**: 2026-09-18  

---

## 1. Identificação Geral da Fonte Primária

- **Órgão Responsável**: Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP) / Ministério da Educação (MEC)
- **Diretoria Responsável**: Diretoria de Estudos Educacionais (DIRED) / Diretoria de Avaliação da Educação Básica (DAEB)
- **Sistema**: Índice de Desenvolvimento da Educação Básica (IDEB)
- **URL Oficial**:
  - [Portal INEP - Resultados do IDEB por Escola](https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb/resultados)
- **Nome do Arquivo Oficial Consolidado**: `divulgacao_pr_consolidado.xlsx` (preservado em `data/raw/ideb/divulgacao_pr_consolidado.xlsx`)
- **Edição Mais Recente**: Edição 2023 (publicada oficialmente em 14 de agosto de 2024).

---

## 2. Metodologia de Composição e Fórmula do IDEB

O IDEB é um indicador sintético que combina simultaneamente duas dimensões complementares da qualidade educacional:
1. **Desempenho Escolar (Aprendizado / Proficiência $N$)**: obtido a partir das provas censitárias do SAEB em Língua Portuguesa e Matemática;
2. **Rendimento Escolar (Fluxo / Progressão $P$)**: obtido a partir das taxas de aprovação apuradas pelo Censo Escolar da Educação Básica.

### 2.1. Fórmula Oficial

$$\text{IDEB} = N \times P$$

Onde:
- **$N$ (Nota Padronizada de Aprendizado)**:

$$N = \frac{\text{Proficiência Língua Portuguesa Padronizada} + \text{Proficiência Matemática Padronizada}}{2}$$

As proficiências das escalas do SAEB (0 a 500) são padronizadas linearmente para o intervalo de **0 a 10**.

- **$P$ (Indicador de Rendimento / Fluxo Escolar)**:

$$P = \frac{1}{\sum_{i=1}^m \frac{1}{p_i}}$$

Onde $p_i$ representa a taxa de aprovação da série/ano escolar $i$ da respectiva etapa e $m$ é o número de anos escolares que compõem a etapa (ex.: 4 anos para os Anos Finais, 3 anos para o Ensino Médio). Trata-se da média harmônica das taxas de aprovação.
- Se a escola tiver aprovação de 100% em todos os anos ($p_i = 1,0$), então $P = 1,0$ e $\text{IDEB} = N$.
- Se houver reprovação ou retenção, $P < 1,0$, reduzindo o valor final do IDEB.

---

## 3. IDEB Observado vs. Metas Projetadas do PDE

Uma distinção institucional crucial para o jornalismo de dados é a diferença entre **resultado realizado** e **meta política/institucional**:

| Variável | Campo na Base | Significado Oficial | Período de Vigência |
| :--- | :--- | :--- | :---: |
| **IDEB Observado** | `ideb_observado` | O resultado efetivamente alcançado pela escola na respectiva edição bienal | 2005 a 2023 |
| **Meta Projetada** | `ideb_meta` | A meta fixada em 2007 pelo Plano de Metas Compromisso Todos pela Educação (PDE) para o horizonte 2007–2021 | 2007 a 2021 |

### Importante sobre as Metas:
1. O ciclo nacional de metas do PDE foi projetado especificamente para o período **2007 a 2021** (visando atingir a média 6,0 no país no bicentenário da Independência em 2022).
2. Na edição de **2023**, o INEP **não publicou novas metas projetadas por escola**, pois o ciclo anterior foi concluído e novas metas nacionais para o novo Plano Nacional de Educação (PNE) ainda estão em tramitação legislativa.
3. As metas projetadas **jamais devem ser tratadas como resultado alcançado**, mas exclusivamente como referencial de expectativa histórica institucional.

---

## 4. Critérios Oficiais de Divulgação e Sigla `ND`

Conforme normas técnicas do INEP:
1. Para ter seu IDEB e médias do SAEB divulgados publicamente, a escola precisa atender a dois critérios concomitantes na respectiva etapa:
   - **Mínimo de 10 estudantes participantes** na prova do SAEB;
   - **Taxa de participação discente de no mínimo 80%** dos matriculados apurados no Censo Escolar.
2. Escolas que participaram da prova mas não atingiram o quórum de 80% de presença discente recebem a anotação **`ND`** (*Não Divulgado por Critério de Participação do INEP*).
3. **Regra Antitravamento**: Casos com `ND` são mantidos como `NaN` numérico com a marcação `status_ideb = 'NAO_DIVULGADO_CRITERIO_INEP'`. **Jamais são preenchidos como 0**.

---

## 5. Edições Bienais Catalogadas no Projeto

| Edição | Anos Iniciais (EF) | Anos Finais (EF) | Ensino Médio | Observações |
| :---: | :---: | :---: | :---: | :--- |
| **2005** | Sim | Sim | Não (Amostral) | Marco inicial do IDEB |
| **2007** | Sim | Sim | Não (Amostral) | Primeiro ano com meta projetada |
| **2009** | Sim | Sim | Não (Amostral) | Consolidação metodológica |
| **2011** | Sim | Sim | Não (Amostral) | Acompanhamento do ciclo PDE |
| **2013** | Sim | Sim | Não (Amostral) | Aplicação conjunta com ANA |
| **2015** | Sim | Sim | Não (Amostral) | Formatação de vírgula tratada no pipeline |
| **2017** | Sim | Sim | Sim (Censitário) | Primeiro ano com IDEB censitário no Ensino Médio |
| **2019** | Sim | Sim | Sim (Censitário) | Última edição pré-pandemia |
| **2021** | Sim | Sim | Sim (Censitário) | Edição sob impacto da pandemia; presença menor na prova |
| **2023** | Sim | Sim | Sim (Censitário) | Edição de retomada pós-pandemia; divulgada em ago/2024 |
| **2025** | Projetado | Projetado | Projetado | Dados de referência preliminar futura |
