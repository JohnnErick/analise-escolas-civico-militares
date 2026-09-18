# Fontes de Dados de Rendimento Escolar (Censo Escolar / INEP)

> **Investigação**: Colégios Cívico-Militares do Paraná  
> **Documento**: Mapeamento das Fontes Oficiais das Taxas de Rendimento Escolar  
> **Data**: 2026-09-18  

---

## 1. Identificação Geral da Fonte Primária

- **Órgão Responsável**: Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP) / Ministério da Educação (MEC)
- **Diretoria Responsável**: Diretoria de Estatísticas Educacionais (DEED) / Coordenação-Geral do Censo da Educação Básica
- **Sistema**: Censo Escolar da Educação Básica — 2ª Etapa: Módulo "Situação do Aluno"
- **URL Oficial**:
  - [Portal INEP - Indicadores Educacionais / Taxas de Rendimento](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/taxas-de-rendimento-escolar)
  - [Servidor Oficial de Download de Estatísticas Educacionais](https://download.inep.gov.br/informacoes_estatisticas/indicadores_educacionais/)
- **Repositório Bruto Local**: `data/raw/rendimento/`

---

## 2. Metodologia de Coleta e Cálculo das Taxas de Rendimento

### 2.1. O Módulo "Situação do Aluno" do Censo Escolar

Diferente da 1ª etapa do Censo Escolar (que coleta matrículas iniciais na última quarta-feira de maio), a **2ª etapa ("Situação do Aluno")** é realizada ao término do ano letivo (março/abril do ano subsequente):
- Cada escola declara nominalmente no Sistema Educacenso o desfecho acadêmico de cada estudante matriculado.
- As categorias de movimento e rendimento são:
  - **Aprovado**: estudante que satisfez os critérios de aproveitamento escolar e assiduidade mínima exigida pela LDB/SEED-PR;
  - **Reprovado**: estudante retido por rendimento insuficiente ou infrequência;
  - **Abandono**: estudante que deixou de frequentar a escola após o encerramento do período letivo sem formalização de transferência regular;
  - **Transferido**: estudante que migrou para outra unidade escolar durante o ano letivo;
  - **Falecido**: estudante falecido no período.

### 2.2. Fórmulas Oficiais de Cálculo das Taxas

As taxas percentuais de rendimento são calculadas considerando como denominador a população de estudantes matriculados que chegaram ao término do período letivo (excluindo-se transferências e falecimentos):

$$\text{Taxa de Aprovação} = \frac{\text{Total de Estudantes Aprovados}}{\text{Total de Alunos com Vínculo Final Aferido}} \times 100$$

$$\text{Taxa de Reprovação} = \frac{\text{Total de Estudantes Reprovados}}{\text{Total de Alunos com Vínculo Final Aferido}} \times 100$$

$$\text{Taxa de Abandono} = \frac{\text{Total de Estudantes em Abandono}}{\text{Total de Alunos com Vínculo Final Aferido}} \times 100$$

Propriedade formal:

$$\text{Taxa de Aprovação} + \text{Taxa de Reprovação} + \text{Taxa de Abandono} \approx 100\%$$

*(Pequenas discrepâncias podem decorrer de arredondamento ou de alunos catalogados como Sem Informação de Rendimento - SIR).*

---

## 3. Edições e Arquivos Obtidos

O projeto realizou o download oficial dos pacotes completos do INEP por escola para o Estado do Paraná:

| Ano de Referência | Arquivo Oficial Primário | URL Oficial de Origem | Formato Original |
| :---: | :--- | :--- | :---: |
| **2017** | `TAXA_REND_2017_ESCOLAS.zip` | `download.inep.gov.br/.../TAXA_REND_2017_ESCOLAS.zip` | XLSX / ODS |
| **2018** | `TX_REND_ESCOLAS_2018.zip` | `download.inep.gov.br/.../TX_REND_ESCOLAS_2018.zip` | XLSX / ODS |
| **2019** | `tx_rend_escolas_2019.zip` | `download.inep.gov.br/.../tx_rend_escolas_2019.zip` | XLSX / ODS |
| **2020** | `tx_rend_escolas_2020.zip` | `download.inep.gov.br/.../tx_rend_escolas_2020.zip` | XLSX / ODS |
| **2021** | `tx_rend_escolas_2021.zip` | `download.inep.gov.br/.../tx_rend_escolas_2021.zip` | XLSX / ODS |
| **2022** | `tx_rend_escolas_2022.zip` | `download.inep.gov.br/.../tx_rend_escolas_2022.zip` | XLSX / ODS |
| **2023** | `tx_rend_escolas_2023.zip` | `download.inep.gov.br/.../tx_rend_escolas_2023.zip` | XLSX / ODS |

---

## 4. Dicionário das Variáveis de Rendimento

### 4.1. Chaves Cadastrais
- `CO_ENTIDADE` / `ID_ESCOLA`: Código INEP do estabelecimento (8 dígitos);
- `SG_UF`: Sigla da Unidade Federativa (`PR`);
- `CO_MUNICIPIO` e `NO_MUNICIPIO`: Código e nome do município;
- `NO_ENTIDADE`: Denominação oficial da escola no Censo;
- `NO_DEPENDENCIA` / `Dependad`: Dependência administrativa (`Estadual`, `Municipal`, `Privada`, `Federal`).

### 4.2. Variáveis de Taxas por Etapa de Ensino
- **Anos Finais do Ensino Fundamental (6º ao 9º ano)**:
  - Aprovação: `1_CAT_FUN_AF` (2021-2023) / `tap_F58` (2017) / `tap_F04` (2018-2020)
  - Reprovação: `2_CAT_FUN_AF` (2021-2023) / `tre_F58` (2017) / `tre_F04` (2018-2020)
  - Abandono: `3_CAT_FUN_AF` (2021-2023) / `tab_F58` (2017) / `tab_F04` (2018-2020)
- **Ensino Médio**:
  - Aprovação: `1_CAT_MED` (2021-2023) / `tap_MED` (2017-2020)
  - Reprovação: `2_CAT_MED` (2021-2023) / `tre_MED` (2017-2020)
  - Abandono: `3_CAT_MED` (2021-2023) / `tab_MED` (2017-2020)
- **Anos Iniciais do Ensino Fundamental (1º ao 5º ano)**:
  - Aprovação: `1_CAT_FUN_AI` (2021-2023) / `tap_F14` (2017-2020)
  - Reprovação: `2_CAT_FUN_AI` (2021-2023) / `tre_F14` (2017-2020)
  - Abandono: `3_CAT_FUN_AI` (2021-2023) / `tab_F14` (2017-2020)

---

## 5. Distinções Conceituais Fundamentais

Para preservar o rigor técnico do jornalismo de dados, o projeto separa estritamente os seguintes conceitos:

| Conceito | Fonte Oficial | O que mede | O que NÃO mede |
| :--- | :--- | :--- | :--- |
| **Aprovação** | Censo Escolar (Situação do Aluno) | Proporção de estudantes que avançaram de série ao final do ano | Não mede nível de proficiência ou aprendizado adquirido na prova |
| **Reprovação** | Censo Escolar (Situação do Aluno) | Proporção de estudantes retidos na série | Não mede abandono nem evasão temporária |
| **Abandono** | Censo Escolar (Situação do Aluno) | Proporção de estudantes que deixaram de frequentar durante aquele ano letivo | Não mede abandono ao longo de vários anos (evasão acumulada) |
| **Matrícula Inicial** | Censo Escolar (1ª Etapa) | Quantidade de estudantes matriculados em maio | Não reflete quantos concluíram o ano |
| **Proficiência** | SAEB (DAEB/INEP) | Desempenho discente em Português e Matemática (escala TRI) | Não reflete diretamente se o estudante foi aprovado ou retido |

---

## 6. Tratamento de Casos Especiais e Valores Ausentes

1. **Símbolos Oficiais nas Tabelas**:
   - `--` (*Não Ofertado / Sem Estudantes*): Etapa não oferecida pela unidade escolar no respectivo ano letivo. Tratado como `NaN` na variável numérica e classificado como `SEM_INFORMACAO_OU_NAO_OFERTADO`.
   - `ND` (*Não Divulgado*): Não aplicável ao Censo Escolar (o Censo é declaratório universal), mas preservado se identificado.
2. **Ausência não é Zero**: Uma escola sem turmas de Ensino Médio tem taxa de abandono ausente (`NaN`), jamais `0,0%`.
3. **Escola `41167090` (CE Andreia Neres dos Santos em Cascavel)**: Criada recentemente (Edital nº 125/2025); não possuía turmas ativas na série histórica do Censo Escolar de 2017 a 2023, sendo categorizada como `FORA_DA_POPULACAO_HISTORICA`.
