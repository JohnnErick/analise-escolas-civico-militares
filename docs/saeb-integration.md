# Documentação da Metodologia de Integração CCM × SAEB

> **Investigação**: Colégios Cívico-Militares do Paraná  
> **Documento**: Arquitetura e Procedimentos de Integração de Dados  
> **Data**: 2026-09-18  
> **Status**: Concluído e Validado  

---

## 1. Visão Geral e Arquitetura do Pipeline

A integração dos dados de avaliação educacional do **SAEB/IDEB** à base histórica dos **Colégios Cívico-Militares (CCM)** do Paraná foi estruturada em um fluxo modular, estritamente determinístico e reprodutível.

```text
Fonte Primária Oficial (INEP/MEC)
        ↓
Arquivo Bruto Consolidado (data/raw/saeb/divulgacao_pr_consolidado.xlsx)
        ↓
Extração Estrutural (scripts/import/importar_saeb_inep.py)
        ↓
Parquets Brutos por Etapa (data/raw/saeb/saeb_*_raw.parquet)
        ↓
Transformação Wide → Tidy & Limpeza (scripts/transform/transformar_saeb_painel.py)
        ↓
Base SAEB Tidy Paraná (data/processed/saeb/saeb_escolas_parana_tidy.*)
        ↓
Matching Cadastral INEP & Auditoria (scripts/transform/integrar_ccm_saeb.py)
        ↓
Bases Integradas Finais:
  ├── ccm_saeb_matriz_integrada.* (2020–2026: Análise do Período Institucional)
  ├── ccm_saeb_serie_historica_completa.* (2005–2025: Análise Longitudinal Completa)
  └── auditoria_matching_ccm_saeb.csv (Auditoria Cadastral 201 Escolas × Anos)
        ↓
Validação de Integridade e Relatório (scripts/validation/validar_integracao_saeb.py)
```

---

## 2. Scripts do Pipeline de Integração

O pipeline é composto por 4 scripts em Python 3 localizados em diretórios específicos:

### 2.1. Ingestão e Validação Estrutural
- **Script**: `scripts/import/importar_saeb_inep.py`
- **Função**: Lê o arquivo `data/raw/saeb/divulgacao_pr_consolidado.xlsx`, valida a integridade das abas de cada etapa de ensino (`divulgacao_anos_iniciais`, `divulgacao_anos_finais`, `divulgacao_ensino_medio`) e verifica a presença das colunas essenciais de cadastro (`ID_ESCOLA`, `NO_ESCOLA`, `SG_UF`, `NO_MUNICIPIO`, `REDE`).
- **Saídas**:
  - `data/raw/saeb/saeb_anos_iniciais_raw.parquet` (2.976 linhas)
  - `data/raw/saeb/saeb_anos_finais_raw.parquet` (1.965 linhas)
  - `data/raw/saeb/saeb_ensino_medio_raw.parquet` (1.704 linhas)

### 2.2. Transformação e Padronização Tidy
- **Script**: `scripts/transform/transformar_saeb_painel.py`
- **Função**:
  - Transforma os dados do formato *wide* (onde cada ano é uma coluna: `VL_NOTA_MATEMATICA_2023`, `VL_NOTA_MATEMATICA_2021`, etc.) para o formato analítico padronizado *tidy / long* (uma linha por escola $\times$ etapa $\times$ ano);
  - Trata formatações numéricas e separadores decimais (garantindo que vírgulas em strings não anulem notas, preservando mais de 3.500 registros de edições como a de 2015);
  - Classifica explicitamente o motivo da ausência de notas na variável `STATUS_PARTICIPACAO_SAEB` (`DIVULGADO`, `NAO_DIVULGADO_CRITERIO_INEP`, `SEM_PARTICIPACAO`, `DADO_AUSENTE`).
- **Saídas**:
  - `data/processed/saeb/saeb_escolas_parana_tidy.parquet` (62.871 linhas)
  - `data/processed/saeb/saeb_escolas_parana_tidy.csv` (delimitado por `;`)

### 2.3. Cruzamento e Integração com a Base CCM
- **Script**: `scripts/transform/integrar_ccm_saeb.py`
- **Função**:
  - Realiza o matching determinístico via código INEP (`codigo_inep` == `ID_ESCOLA`);
  - Gera a auditoria cadastral de todas as 201 escolas CCM contra a base do SAEB;
  - Realiza o merge temporal entre a matriz histórica das escolas (`historico_ccm_por_ano.csv`) e as edições do SAEB, preservando integralmente o status institucional auditado (`SIM`, `NAO`, `INDETERMINADO`);
  - Diferencia anos sem aplicação censitária do SAEB com o rótulo `SEM_EDICAO_SAEB_ANO_PAR_OU_INTERMEDIARIO`.
- **Saídas**:
  - `data/processed/saeb/ccm_saeb_matriz_integrada.parquet` e `.csv` (2.646 linhas: 2020 a 2026 por escola e etapa);
  - `data/processed/saeb/ccm_saeb_serie_historica_completa.parquet` e `.csv` (3.198 linhas: 2005 a 2025 longitudinal);
  - `data/processed/saeb/auditoria_matching_ccm_saeb.csv` (2.211 linhas de auditoria).

### 2.4. Validação Rigorosa de Integridade
- **Script**: `scripts/validation/validar_integracao_saeb.py`
- **Função**: Valida a contagem de escolas antes e depois da junção, verifica duplicidades, audita a distribuição do matching, afere as taxas de preenchimento das variáveis do SAEB e emite o parecer conclusivo.
- **Saída**: `docs/saeb-validation.md`

---

## 3. Estrutura dos Arquivos de Dados Produzidos

### 3.1. Matriz Integrada do Período Institucional (`ccm_saeb_matriz_integrada.csv/.parquet`)
Contém a visão do período de vigência e expansão do programa CCM (2020 a 2026):

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `codigo_inep` | Int64 | Código oficial de 8 dígitos do INEP |
| `escola` | String | Nome da escola conforme atos oficiais |
| `municipio` | String | Município do estabelecimento |
| `ano` | Int64 | Ano letivo (2020, 2021, 2022, 2023, 2024, 2025, 2026) |
| `status_ccm` | String | Situação institucional: `SIM`, `NAO` ou `INDETERMINADO` (da base auditada) |
| `ano_inicio_ccm` | Float64 | Ano oficial de implantação do modelo (ex: 2021, 2024, 2026) |
| `ano_saida_ccm` | Float64 | Ano de eventual descontinuidade (quando houver) |
| `ETAPA` | String | Etapa de ensino: `Anos Finais (6º-9º)`, `Ensino Médio` ou `Anos Iniciais (1º-5º)` |
| `SAEB_MATEMATICA` | Float64 | Proficiência média na escala Saeb em Matemática (0 a 500) |
| `SAEB_PORTUGUES` | Float64 | Proficiência média na escala Saeb em Língua Portuguesa (0 a 500) |
| `SAEB_NOTA_MEDIA` | Float64 | Média padronizada $N$ calculada pelo INEP (0 a 10) |
| `IDEB_OBSERVADO` | Float64 | Índice de Desenvolvimento da Educação Básica oficial |
| `INDICADOR_RENDIMENTO`| Float64 | Indicador de rendimento/fluxo escolar calculado pelo INEP |
| `TAXA_APROVACAO` | Float64 | Taxa oficial de aprovação discente |
| `STATUS_PARTICIPACAO_SAEB` | String | Motivo do status: `DIVULGADO`, `NAO_DIVULGADO_CRITERIO_INEP`, `SEM_PARTICIPACAO`, `SEM_EDICAO_SAEB_ANO_PAR_OU_INTERMEDIARIO` |

### 3.2. Série Histórica Longitudinal Completa (`ccm_saeb_serie_historica_completa.csv/.parquet`)
Contém a trajetória das escolas cívico-militares em todas as edições do SAEB realizadas pelo INEP desde 2005 até a última edição divulgada, permitindo a futura análise de tendências pré-intervenção (diferenças em diferenças, séries temporais interrompidas ou synthetic controls).

---

## 4. Auditoria de Matching e Cobertura

O matching das 201 escolas cívico-militares contra o cadastro de divulgação do SAEB/IDEB do INEP resultou em:

- **200 escolas `CONFIRMADO` (99,5%)**: Código INEP idêntico, município e nome convergentes;
- **1 escola `AMBÍGUO` (0,5%)**: Código `41146093` (auditado na fase anterior como erro material do Edital 125/2025, retificado pelo Edital 136/2025 para `41016254`). O código permanece isolado e documentado;
- **0 escolas `NAO_ENCONTRADO` (0,0%)**: Nenhuma escola da base CCM foi perdida;
- **0 pendências `REVISAR` (0,0%)**.

---

## 5. Instruções de Reprodutibilidade Completa

Para reexecutar integralmente todo o pipeline de importação, transformação, integração e validação do SAEB, utilize os seguintes comandos a partir da raiz do repositório:

```bash
# 1. Ingestão dos dados brutos oficiais do SAEB
python3 scripts/import/importar_saeb_inep.py

# 2. Transformação analítica wide -> tidy e limpeza de strings numéricas
python3 scripts/transform/transformar_saeb_painel.py

# 3. Integração com a matriz histórica CCM e auditoria cadastral
python3 scripts/transform/integrar_ccm_saeb.py

# 4. Execução dos testes estatísticos de validação e emissão do relatório
python3 scripts/validation/validar_integracao_saeb.py
```
