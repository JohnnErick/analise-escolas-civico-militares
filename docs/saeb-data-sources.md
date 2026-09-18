# Panorama e Detalhamento das Fontes de Dados do SAEB

> **Investigação**: Colégios Cívico-Militares do Paraná  
> **Documento**: Levantamento Oficial de Fontes e Edições do SAEB/IDEB  
> **Data**: 2026-09-18  

---

## 1. Visão Geral do Sistema de Avaliação da Educação Básica (SAEB)

O **Sistema de Avaliação da Educação Básica (SAEB)**, gerido pelo Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP), é o principal instrumento de avaliação em larga escala da qualidade da educação básica brasileira.

Juntamente com os dados de aprovação, reprovação e abandono apurados pelo Censo Escolar, as notas de proficiência do SAEB compõem o **Índice de Desenvolvimento da Educação Básica (IDEB)**.

---

## 2. Levantamento Histórico das Edições Disponíveis (2005 a 2023)

O SAEB ocorre bienalmente em anos ímpares. O quadro a seguir detalha a disponibilidade, cobertura e características de cada edição para o Estado do Paraná:

| Ano / Edição | Abrangência da Avaliação | Disponibilidade de Microdados | Disponibilidade por Escola | Vinculação por Código INEP | Limitações e Observações Metodológicas |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **2005** | Anos Iniciais e Finais (Censitário); EM (Amostral) | Sim | Sim (EF) | Sim (`ID_ESCOLA`) | Marco inicial do IDEB; Ensino Médio com divulgação censitária restrita. |
| **2007** | Anos Iniciais e Finais (Censitário); EM (Amostral) | Sim | Sim (EF) | Sim (`ID_ESCOLA`) | Consolidação do modelo censitário no Ensino Fundamental público. |
| **2009** | Anos Iniciais e Finais (Censitário); EM (Amostral) | Sim | Sim (EF) | Sim (`ID_ESCOLA`) | Estabilidade metodológica da escala de proficiência. |
| **2011** | Anos Iniciais e Finais (Censitário); EM (Amostral) | Sim | Sim (EF) | Sim (`ID_ESCOLA`) | Introdução de questionários contextuais aperfeiçoados. |
| **2013** | Anos Iniciais e Finais (Censitário); EM (Amostral) | Sim | Sim (EF) | Sim (`ID_ESCOLA`) | Avaliação nacional da alfabetização (ANA) aplicada em paralelo. |
| **2015** | Anos Iniciais e Finais (Censitário); EM (Amostral) | Sim | Sim (EF) | Sim (`ID_ESCOLA`) | Formatação numérica mista em planilhas originais (vírgula decimal tratada no pipeline). |
| **2017** | EF e Ensino Médio Público (Censitário) | Sim | Sim (EF e EM) | Sim (`ID_ESCOLA`) | Primeiro ano de universalização censitária para o Ensino Médio público regular. |
| **2019** | EF e Ensino Médio (Censitário) | Sim | Sim (EF e EM) | Sim (`ID_ESCOLA`) | Última edição pré-pandemia de COVID-19; referência de ápice histórico do ciclo anterior. |
| **2021** | EF e Ensino Médio (Censitário com adesão) | Sim | Sim (EF e EM) | Sim (`ID_ESCOLA`) | **Impacto da Pandemia**: Menor taxa de presença discente; maior incidência de `ND` devido ao critério de 80% de participação. |
| **2023** | EF e Ensino Médio (Censitário) | Sim | Sim (EF e EM) | Sim (`ID_ESCOLA`) | Edição de recuperação pós-pandemia; divulgação oficial em agosto/2024. |

---

## 3. Unidade de Análise, Identificadores e Chave de Ligação

### 3.1. Chave Primária de Ligação Cadastral

- **Identificador Universal INEP**: `CO_ENTIDADE` (nos microdados do Censo Escolar e arquivos de dados abertos) ou `ID_ESCOLA` (nas planilhas de divulgação oficial do SAEB/IDEB).
- **Características**: Código numérico inteiro de 8 dígitos atribuído unicamente a cada estabelecimento de ensino no Brasil.
- **Correspondência**: O campo `ID_ESCOLA` presente na base de divulgação do SAEB é 100% idêntico ao campo `codigo_inep` presente na base consolidada dos Colégios Cívico-Militares do Paraná (`historico_ccm_por_ano.csv` e `historico_ccm_matching_inep.csv`).

### 3.2. Relação Estrutural de Dados

```text
Cadastro INEP (CO_ENTIDADE)
         ↓
SAEB Escola (ID_ESCOLA)
         ↓
Etapa de Ensino (Anos Iniciais / Anos Finais / Ensino Médio)
         ↓
Ano da Edição (2005 ... 2023)
```

Nenhum cruzamento entre as bases utiliza o nome da escola ou município como chave primária. Nome e município são mantidos exclusivamente para auditoria descritiva e detecção de anomalias cadastrais.

---

## 4. Indicadores de Proficiência e Metodologia da Escala Saeb

### 4.1. Escala de Proficiência do SAEB

As proficiências médias das escolas são apresentadas em uma escala construída por meio da **Teoria da Resposta ao Item (TRI)**:

- **Língua Portuguesa**: Escala contínua de 0 a 500 pontos, historicamente calibrada com média 250 e desvio padrão 50 (referência Saeb 1997). Mede a capacidade discente de compreensão textual, inferência, localização de informações e coerência argumentativa.
- **Matemática**: Escala contínua de 0 a 500 pontos, historicamente calibrada com média 250 e desvio padrão 50 (referência Saeb 1997). Mede a capacidade discente de resolução de problemas, cálculo numérico, álgebra, geometria e tratamento da informação.

### 4.2. Variável Padronizada $N$ e Composição do IDEB

O INEP calcula a nota média padronizada $N$ da escola por meio de uma transformação linear das notas da escala TRI para uma escala simplificada de 0 a 10:

$$N = \frac{\text{Proficiência Língua Portuguesa Padronizada} + \text{Proficiência Matemática Padronizada}}{2}$$

O IDEB é o produto dessa proficiência padronizada pelo indicador de rendimento escolar $P$ (baseado nas taxas de aprovação dos anos escolares da etapa):

$$\text{IDEB} = N \times P$$

Onde $P = \frac{1}{\sum \frac{1}{p_i}}$ representa a média harmônica das taxas de aprovação de cada série componente da etapa.

---

## 5. Microdados Amostrais vs. Resultados Agregados Oficiais Escolares

### 5.1. Comparação Metodológica

| Critério | Microdados Discentes (`TS_ALUNO`) | Resultados Agregados Oficiais por Escola |
| :--- | :--- | :--- |
| **Unidade de Linha** | Estudante individual | Escola $\times$ Etapa de Ensino |
| **Tratamento de Pesos** | Exige aplicação do peso amostral discente (`PESO_ALUNO`) de pós-estratificação | Ponderações e calibrações já computadas e validadas pela diretoria estatística do INEP |
| **Risco Metodológico** | Pequenas divergências de arredondamento ou descarte de itens podem gerar médias diferentes dos dados públicos | Totalmente alinhado e idêntico às divulgações oficiais do MEC, INEP e SEED/PR |
| **Consistência Jornalística** | Permite recortes sociodemográficos internos (raça, renda familiar) | Fornece os indicadores oficiais de transparência pública utilizados para prestação de contas |

### 5.2. Diretriz de Adoção do Projeto

Adotou-se como fonte analítica primária a **base oficial de resultados agregados por escola divulgada pelo INEP**. Isso garante que todo valor apresentado pelo projeto para uma escola específica seja rigorosamente o mesmo divulgado nas plataformas do governo federal e estadual.

---

## 6. Critérios Oficiais de Divulgação do INEP e Tratamento de Ausências

### 6.1. Regras Institucionais

De acordo com as normas oficiais do INEP:
1. Uma escola só tem suas notas divulgadas se atender simultaneamente a:
   - Presença mínima de **10 estudantes** na etapa avaliada;
   - Taxa de participação discente de pelo menos **80%** dos alunos matriculados na etapa (apurados no Censo Escolar).
2. Casos abaixo do patamar de 80% ou com menos de 10 estudantes recebem o código **`ND`** (*Não Divulgado*).
3. Etapas não ofertadas ou escolas sem estudantes matriculados recebem o símbolo **`-`**.

### 6.2. Postura Antitravamento e Integridade dos Dados

- **NUNCA substituir `ND` ou `-` por 0**: Atribuir valor zero falsearia grosseiramente a média do colégio e da rede de ensino.
- **`ND` não significa baixo desempenho**: Uma escola de alto rendimento que teve 79% de presença discente terá nota registrada como `ND`, sem que isso indique falha pedagógica.
- **Categorização Explícita**: Na base processada, a coluna `STATUS_PARTICIPACAO_SAEB` diferencia com precisão:
  - `DIVULGADO`: Nota numérica oficial presente;
  - `NAO_DIVULGADO_CRITERIO_INEP`: Participou, mas sem quórum de divulgação;
  - `SEM_PARTICIPACAO`: Não participou ou etapa não ofertada;
  - `SEM_EDICAO_SAEB_ANO_PAR_OU_INTERMEDIARIO`: Anos em que não houve avaliação censitária nacional (2020, 2022, 2024, 2026).

---

## 7. Constatação Crítica: Linha de Base (Baseline) vs. Efeito Institucional

Ao integrar a base histórica CCM com as edições do SAEB de 2021 e 2023, constata-se um elemento cronológico central:

1. **Adesão Temporal das Escolas**:
   - 106 escolas CCM iniciaram suas operações sob o modelo militar em **2024** (Editais nº 107/2023 e 128/2023);
   - 33 escolas CCM têm previsão de início em **2026** (Edital nº 125/2025 retificado pelo Edital nº 136/2025);
   - Apenas colégios pioneiros aderiram em anos anteriores.
2. **Implicação**:
   - Os resultados das edições do SAEB de **2021 e 2023** para mais de 70% das escolas CCM documentam seu **desempenho histórico enquanto escolas públicas regulares** (período de *baseline* ou pré-intervenção).
   - O projeto preserva essa distinção na coluna temporal `status_ccm` correspondente ao ano da edição, impedindo inferências distorcidas ou afirmações anacrônicas.
