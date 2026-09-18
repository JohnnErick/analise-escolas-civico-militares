# Fontes Oficiais de Dados do Projeto

> **Investigação**: Colégios Cívico-Militares do Paraná  
> **Última Atualização**: 2026-09-18  
> **Status**: Ativo e Auditado  

Este documento cataloga de forma estruturada e transparente todas as fontes oficiais primárias utilizadas na investigação jornalística sobre os Colégios Cívico-Militares (CCM) do Paraná.

Em estrita observância ao rigor metodológico do projeto, **não são utilizadas bases agregadas de terceiros ou fontes não governamentais como fontes primárias**.

---

## 1. Atos Normativos e Editais Oficiais da SEED/PR

- **Órgão Responsável**: Secretaria de Estado da Educação do Paraná (SEED/PR) / Governo do Estado do Paraná
- **Origem dos Documentos**: Diário Oficial Executivo do Estado do Paraná (DIOE/PR) e Portal Oficial de Editais da SEED/PR
- **Repositório Interno**: `biblioteca de ref/`
- **Total de Documentos Catalogados**: 50 documentos oficiais (508 páginas auditadas)
- **Tipologia**:
  - Leis Complementares e Ordinárias (ex.: Lei nº 20.338/2020 de criação do programa CCM);
  - Decretos Estaduais de regulamentação e criação de colégios;
  - Resoluções da SEED/PR instituindo o modelo nas unidades escolares;
  - Editais de Consulta Pública à Comunidade Escolar e Editais de Homologação de Resultados;
  - Portarias e Informações Técnicas da SEED/PR.
- **Formato Original**: PDF (texto pesquisável e páginas digitalizadas auditadas).
- **Processamento no Projeto**:
  - Extração literal: `scripts/extrair_texto_literal.py`
  - Estruturação de evidências: `scripts/estruturar_evidencias_ccm.py`
  - Base gerada: `data/processed/historico_ccm_eventos.csv` (384 eventos documentais)

---

## 2. Cadastro Oficial de Estabelecimentos de Ensino (INEP/MEC)

- **Órgão Responsável**: Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP) / Ministério da Educação (MEC)
- **Base de Referência**: Cadastro das Escolas do Censo Escolar da Educação Básica / Catálogo de Escolas
- **URL Oficial**: [INEP - Microdados do Censo da Educação Básica](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar) e [Catálogo de Escolas INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/bases-de-dados/escolas)
- **Formato**: CSV / XLSX / Parquet
- **Unidade de Observação**: Escola (`CO_ENTIDADE` / `codigo_inep`)
- **Abrangência**: Estabelecimentos de ensino do Estado do Paraná (rede estadual, municipal, federal e privada)
- **Utilização no Projeto**:
  - Chave de ligação unívoca de 8 dígitos para cada escola (`codigo_inep`);
  - Normalização padronizada do nome oficial da escola e município;
  - Validação cadastral: `scripts/executar_matching_inep.py`
  - Base gerada: `data/processed/historico_ccm_matching_inep.csv` (201 escolas auditadas, 100% localizadas no cadastro oficial).

---

## 3. SAEB — Sistema de Avaliação da Educação Básica

### 3.1. Identificação Geral da Fonte
- **Órgão Responsável**: Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP) / Diretoria de Avaliação da Educação Básica (DAEB)
- **Sistema**: Sistema de Avaliação da Educação Básica (SAEB)
- **URL Oficial**: [Portal INEP - Resultados do Saeb](https://www.gov.br/inep/pt-br/areas-de-atuacao/avaliacao-e-exames-educacionais/saeb/resultados)
- **Nome do Arquivo Primário**: `divulgacao_pr_consolidado.xlsx` (armazenado em `data/raw/saeb/divulgacao_pr_consolidado.xlsx`)
- **Data de Publicação Oficial**: 14 de agosto de 2024 (Edição 2023)
- **Formato**: Planilha oficial consolidada (XLSX) e microdados amostrais discentes (CSV).
- **Unidade de Observação**: Escola (`ID_ESCOLA`), vinculada a cada etapa (`ETAPA`) e edição bienal (`ANO_SAEB`).
- **Variáveis Principais**:
  - `SAEB_PORTUGUES`: Proficiência média na escala TRI (0 a 500)
  - `SAEB_MATEMATICA`: Proficiência média na escala TRI (0 a 500)
  - `SAEB_NOTA_MEDIA`: Nota padronizada $N$ calculada pelo INEP (0 a 10)

---

## 4. Rendimento Escolar (Censo Escolar / INEP)

### 4.1. Identificação Geral da Fonte
- **Órgão Responsável**: Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP) / Diretoria de Estatísticas Educacionais (DEED)
- **Sistema**: Censo Escolar da Educação Básica — Módulo "Situação do Aluno" (2ª Etapa)
- **URL Oficial**: [Portal INEP - Taxas de Rendimento Escolar](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/taxas-de-rendimento-escolar)
- **Servidor de Download**: `https://download.inep.gov.br/informacoes_estatisticas/indicadores_educacionais/{ano}/tx_rend_escolas_{ano}.zip`
- **Repositório Bruto Local**: `data/raw/rendimento/` (arquivos compactados de 2017 a 2023)
- **Periodicidade**: Anual (coleta e publicação a cada ano letivo concluído).

### 4.2. Unidade de Observação e Variáveis
- **Unidade de Observação**: Escola (`CO_ENTIDADE` / `ID_ESCOLA`), etapa de ensino e ano civil.
- **Variáveis Principais**:
  - `TAXA_APROVACAO`: Percentual de estudantes aprovados ao final do ano letivo (0,0% a 100,0%);
  - `TAXA_REPROVACAO`: Percentual de estudantes retidos na série (0,0% a 100,0%);
  - `TAXA_ABANDONO`: Percentual de estudantes que deixaram de frequentar no ano (0,0% a 100,0%).
- **População**: Alunos matriculados que atingiram o término do período letivo (excluindo-se transferências e falecimentos).

---

## 5. IDEB — Índice de Desenvolvimento da Educação Básica

### 5.1. Identificação Geral da Fonte
- **Órgão Responsável**: INEP / MEC (DIRED e DAEB)
- **Sistema**: Índice de Desenvolvimento da Educação Básica (IDEB)
- **URL Oficial**: [Portal INEP - Resultados do Ideb](https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb/resultados)
- **Arquivo Oficial Consolidado**: `divulgacao_pr_consolidado.xlsx` (preservado em `data/raw/ideb/divulgacao_pr_consolidado.xlsx`)
- **Periodicidade**: Bienal (anos ímpares: 2005 a 2023).

### 5.2. Metodologia e Composição
- **Fórmula Oficial**: $\text{IDEB} = N \times P$
  - $N$: média padronizada das proficiências do SAEB (escala 0 a 10);
  - $P$: média harmônica das taxas de aprovação das séries componentes (indicador de rendimento).
- **Variáveis Principais**:
  - `IDEB_OBSERVADO`: Resultado efetivamente realizado na edição (escala 0,0 a 10,0);
  - `IDEB_META`: Meta institucional projetada pelo Plano de Metas PDE (ciclo 2007–2021);
  - `IDEB_COMPONENTE_N` e `IDEB_COMPONENTE_P`: Fatores componentes do cálculo oficial.

---

---

## 6. Dimensão Cadastral e Georreferenciamento das Escolas

### 6.1. Fontes Primárias do Cadastro
1. **INEP / Censo Escolar da Educação Básica 2023**:
   - **Arquivo**: `data/raw/rendimento/tx_rend_escolas_2023/tx_rend_escolas_2023.xlsx`
   - **Variáveis**: Código INEP (`CO_ENTIDADE`), Nome Oficial (`NO_ENTIDADE`), Código IBGE do Município (`CO_MUNICIPIO`), Nome do Município (`NO_MUNICIPIO`), Localização (`NO_CATEGORIA` — Urbana/Rural), Dependência Administrativa (`NO_DEPENDENCIA` — Estadual/Municipal/Federal/Privada) e Etapas Ofertadas (`1_CAT_FUN_AI`, `1_CAT_FUN_AF`, `1_CAT_MED`).
2. **SEED/PR / Atos e Editais Oficiais (2020 a 2025)**:
   - **Arquivos**: Editais de consulta pública e homologação CCM em `data/extracted/editais/*.txt`.
   - **Variáveis**: Núcleo Regional de Educação (`NRE`), Nome Oficial nos Editais (`nome_original_edital`), Data e Ano de Implantação (`ano_inicio_ccm`).
3. **SEED/PR / Georreferenciamento Oficial (KML)**:
   - **Arquivo**: `planilha ref/Colégios Cívico-Militares do Paraná.kml` e `data/mapeamento_escolas_civico_militares.csv`.
   - **Variáveis**: Coordenadas geográficas exatas (`LATITUDE`, `LONGITUDE`), identificadas com o tipo `EXATA_KML`.
4. **IBGE / Malha Municipal e Coordenadas**:
   - **Arquivo**: `data/municipios_pr.csv`.
   - **Variáveis**: Centroide geográfico municipal (`latitude`, `longitude`) atribuído com o tipo `CENTROIDE_MUNICIPIO` para escolas sem ponto individual no KML.

### 6.2. Regra de Dados Ausentes
- Os campos **Endereço (logradouro)**, **Bairro** e **CEP** não constam nas matrizes tabulares oficiais de dados abertos disponíveis no ambiente local.
- Em estrito cumprimento às normas metodológicas, **esses campos são mantidos como `None` / ausentes**, sendo vedada qualquer imputação ou invenção de dados.

---

## 7. Rastreabilidade e Reprodutibilidade Completa

| Etapa | Script | Entrada Primária | Saída Consolidada |
| :--- | :--- | :--- | :--- |
| **Importação SAEB** | `scripts/import/importar_saeb_inep.py` | `divulgacao_pr_consolidado.xlsx` | `data/raw/saeb/*.parquet` |
| **Transformação SAEB** | `scripts/transform/transformar_saeb_painel.py` | `data/raw/saeb/*.parquet` | `data/processed/saeb/saeb_escolas_parana_tidy.*` |
| **Importação Rendimento** | `scripts/import/importar_rendimento_inep.py` | `tx_rend_escolas_{ano}.zip` | `data/raw/rendimento/rendimento_parana_raw.parquet` |
| **Transformação Rendimento** | `scripts/transform/transformar_rendimento_painel.py` | `rendimento_parana_raw.parquet` | `data/processed/rendimento/rendimento_escolas_parana_tidy.*` |
| **Importação IDEB** | `scripts/import/importar_ideb_inep.py` | `divulgacao_pr_consolidado.xlsx` | `data/raw/ideb/ideb_*_raw.parquet` |
| **Transformação IDEB** | `scripts/transform/transformar_ideb_painel.py` | `ideb_*_raw.parquet` | `data/processed/ideb/ideb_escolas_parana_tidy.*` |
| **Importação Cadastro** | `scripts/import/importar_cadastro_escolas.py` | Censo 2023 + Editais SEED + KML + IBGE | Memória / Extrações Intermediárias |
| **Transformação Cadastro** | `scripts/transform/transformar_cadastro_escolas.py` | Censo 2023 + Editais + KML + IBGE | `data/processed/escolas_cadastro.*` |
| **Validação Cadastro** | `scripts/validation/validar_cadastro_escolas.py` | Dimensão Mestre + Histórico CCM | `data/validation/auditoria_cadastro_escolas.md` |
| **Integração Plena** | `scripts/transform/integrar_ccm_saeb_rendimento_ideb.py` | Bases CCM + SAEB + Rendimento + IDEB | `data/processed/ccm_saeb_rendimento_ideb.*` |
| **Validação Automatizada** | `scripts/validation/validar_integracao_rendimento_ideb.py` | Matriz preliminar integrada | `docs/rendimento-ideb-validation.md` |
