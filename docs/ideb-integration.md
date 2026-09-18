# Integração dos Dados do IDEB (Índice de Desenvolvimento da Educação Básica)

> **Investigação**: Colégios Cívico-Militares do Paraná  
> **Documento**: Metodologia e Pipeline de Integração dos Resultados do IDEB  
> **Data**: 2026-09-18  
> **Status**: Concluído e Validado  

---

## 1. Visão Geral e Arquitetura do Pipeline

A integração dos dados oficiais do IDEB à base histórica CCM segue um fluxo estruturado e reprodutível:

```text
Planilha Consolidada INEP (data/raw/ideb/divulgacao_pr_consolidado.xlsx)
        ↓
Importação por Etapa (scripts/import/importar_ideb_inep.py)
        ↓
Parquets Brutos por Etapa (data/raw/ideb/ideb_*_raw.parquet)
        ↓
Transformação Wide → Tidy & Limpeza (scripts/transform/transformar_ideb_painel.py)
        ↓
Base IDEB Tidy (data/processed/ideb/ideb_escolas_parana_tidy.parquet)
        ↓
Integração com a Base Histórica CCM (scripts/transform/integrar_ccm_saeb_rendimento_ideb.py)
        ↓
Base Integrada Final: ccm_saeb_rendimento_ideb.*
```

---

## 2. Scripts do Pipeline do IDEB

### 2.1. Ingestão dos Dados Consolidados Oficiais
- **Script**: `scripts/import/importar_ideb_inep.py`
- **Operação**:
  - Lê o arquivo oficial `divulgacao_pr_consolidado.xlsx` divulgado pelo INEP para o Paraná;
  - Extrai as três abas oficiais: Anos Iniciais (`divulgacao_anos_iniciais`), Anos Finais (`divulgacao_anos_finais`) e Ensino Médio (`divulgacao_ensino_medio`);
  - Valida a presença das variáveis fundamentais de identificação (`ID_ESCOLA`, `NO_ESCOLA`, `CO_MUNICIPIO`, `SG_UF`, `REDE`).
- **Saídas**:
  - `data/raw/ideb/ideb_anos_iniciais_raw.parquet` (2.976 linhas)
  - `data/raw/ideb/ideb_anos_finais_raw.parquet` (1.965 linhas)
  - `data/raw/ideb/ideb_ensino_medio_raw.parquet` (1.704 linhas)

### 2.2. Transformação Analítica Tidy
- **Script**: `scripts/transform/transformar_ideb_painel.py`
- **Operação**:
  - Converte as colunas por edição bienal (`VL_OBSERVADO_{ano}`, `VL_PROJECAO_{ano}`, `VL_NOTA_MEDIA_{ano}`, `VL_INDICADOR_REND_{ano}`, `VL_APROVACAO_{ano}_SI_4`) para o formato *tidy* por `(ID_ESCOLA x ANO_IDEB x ETAPA)`;
  - Saneia separadores decimais e strings (`ND`, `-`);
  - Preserva as metas projetadas do PDE como variável independente (`ideb_meta`);
  - Categoriza o status na variável `STATUS_IDEB`.
- **Saídas**:
  - `data/processed/ideb/ideb_escolas_parana_tidy.parquet` (62.871 registros)
  - `data/processed/ideb/ideb_escolas_parana_tidy.csv`

---

## 3. Chave Primária e Regras de Matching

- **Chave Primária de Ligação**: `codigo_inep` $\leftrightarrow$ `ID_ESCOLA`, associado a `ano` $\leftrightarrow$ `ANO_IDEB` e à etapa de ensino (`etapa_ensino`).
- **Auditoria de Correspondência Cadastral**:
  - **201 de 201 escolas CCM localizadas no cadastro oficial do IDEB (100,0%)**;
  - **Zero perdas cadastrais**;
  - **Zero duplicidades**.

---

## 4. Relação Estrutural: SAEB, Rendimento e IDEB

A documentação metodológica do projeto estabelece formalmente a relação não-independente entre os três blocos de indicadores:

```text
SAEB (Proficiência)     ──┐
(Escala TRI 0 a 500)      │
                          ├─►  IDEB = N x P
Rendimento (Fluxo)      ──┤    (Escala Sintética 0 a 10)
(Censo Escolar 0 a 100%) ─┘
```

### Advertências Analíticas Essenciais:
1. **Evitar Colinearidade**: O IDEB **não deve ser incluído simultaneamente com o SAEB e o Rendimento** no mesmo modelo econométrico de regressão, pois ele é uma combinação determinística linear-harmônica de ambos.
2. **Defasagem Temporal Zero**: O INEP calcula o IDEB de um dado ano $t$ utilizando o desempenho no SAEB do ano $t$ e as taxas de aprovação do Censo Escolar do próprio ano $t$. Portanto, os componentes são perfeitamente contemporâneos na mesma edição.
3. **Anos Pares**: Como o SAEB e o IDEB ocorrem bienalmente em anos ímpares, os anos pares (2020, 2022, 2024, 2026) possuem `status_ideb = 'SEM_EDICAO_IDEB_ANO_PAR_OU_INTERMEDIARIO'`, mantendo-se como `NaN` analítico.

---

## 5. Dicionário das Variáveis Integradas do IDEB

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `ideb_observado` | Float64 | IDEB oficial apurado na edição (escala de 0,0 a 10,0) |
| `ideb_meta` | Float64 | Meta projetada do PDE para aquela edição (vigente até 2021) |
| `ideb_componente_n` | Float64 | Nota média padronizada de aprendizado ($N$, escala 0 a 10) |
| `ideb_componente_p` | Float64 | Indicador de rendimento escolar ($P$, média harmônica das taxas) |
| `taxa_aprovacao_ideb` | Float64 | Taxa média de aprovação total ponderada da etapa |
| `status_ideb` | String | Situação: `DIVULGADO`, `NAO_DIVULGADO_CRITERIO_INEP`, `SEM_PARTICIPACAO`, `SEM_EDICAO_IDEB_ANO_PAR_OU_INTERMEDIARIO` |
