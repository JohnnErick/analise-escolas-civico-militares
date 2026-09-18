# Integração dos Dados de Rendimento Escolar (Censo Escolar / INEP)

> **Investigação**: Colégios Cívico-Militares do Paraná  
> **Documento**: Metodologia e Pipeline de Integração das Taxas de Rendimento  
> **Data**: 2026-09-18  
> **Status**: Concluído e Validado  

---

## 1. Visão Geral e Arquitetura do Pipeline

A integração das taxas anuais de rendimento escolar (Aprovação, Reprovação e Abandono) segue um fluxo determinístico que parte dos arquivos compactados oficiais do INEP e desemboca na matriz unificada do projeto:

```text
Pacotes Oficiais INEP (data/raw/rendimento/tx_rend_escolas_{ano}.zip)
        ↓
Extração e Filtragem Estadual (scripts/import/importar_rendimento_inep.py)
        ↓
Parquet Bruto Paraná (data/raw/rendimento/rendimento_parana_raw.parquet)
        ↓
Transformação Wide → Tidy & Limpeza (scripts/transform/transformar_rendimento_painel.py)
        ↓
Base Rendimento Tidy (data/processed/rendimento/rendimento_escolas_parana_tidy.parquet)
        ↓
Integração com a Base Histórica CCM (scripts/transform/integrar_ccm_saeb_rendimento_ideb.py)
        ↓
Base Integrada Final: ccm_saeb_rendimento_ideb.*
```

---

## 2. Scripts do Pipeline de Rendimento

### 2.1. Ingestão e Filtragem de Dados Brutos
- **Script**: `scripts/import/importar_rendimento_inep.py`
- **Operação**:
  - Lê os arquivos oficiais de 2017 a 2023 descompactados diretamente do fluxo zip do INEP;
  - Utiliza o motor de leitura otimizado `calamine` para processar com alto desempenho planilhas com mais de 128.000 linhas nacionais;
  - Filtra rigorosamente os estabelecimentos de ensino do Paraná (`SG_UF == 'PR'`);
  - Padroniza a nomenclatura de colunas posicionais estáveis (ano, município, código da escola, taxas por etapa).
- **Saída**: `data/raw/rendimento/rendimento_parana_raw.parquet` (42.182 registros de escola $\times$ ano).

### 2.2. Transformação Analítica Tidy
- **Script**: `scripts/transform/transformar_rendimento_painel.py`
- **Operação**:
  - Pivota os dados para a estrutura canônica: uma linha por `(ID_ESCOLA x ANO x ETAPA)`;
  - Saneia caracteres de separador decimal (conversão robusta de vírgula para ponto);
  - Trata strings não numéricas (`--`, `-`, `ND`);
  - Aplica validação de domínio percentual $[0,0\%, 100,0\%]$;
  - Categoriza o status na variável `STATUS_RENDIMENTO`.
- **Saídas**:
  - `data/processed/rendimento/rendimento_escolas_parana_tidy.parquet` (126.546 registros)
  - `data/processed/rendimento/rendimento_escolas_parana_tidy.csv`

---

## 3. Chave Primária e Regras de Matching

- **Chave de Ligação**: `codigo_inep` $\leftrightarrow$ `CO_ENTIDADE` / `ID_ESCOLA`, acrescida da chave temporal `ano` e da etapa de ensino `etapa_ensino`.
- **Resultado do Matching Cadastral**:
  - **200 de 201 escolas CCM localizadas com sucesso (99,5%)**;
  - **1 caso especial**: Escola `41167090` (Colégio Estadual Professora Andreia Neres dos Santos em Cascavel), criada formalmente pelo Edital nº 125/2025, não possuía turmas em funcionamento no ciclo 2017–2023, sendo categorizada justificadamente como `FORA_DA_POPULACAO_HISTORICA`.
  - **Zero perdas e zero duplicidades**.

---

## 4. Tratamento Antitravamento de Valores Ausentes

- **Ausência mantida como `NaN`**: Nenhuma taxa ausente foi preenchida como zero. Se uma escola de Ensino Fundamental não oferta Ensino Médio, as taxas de Ensino Médio permanecem como `NaN`.
- **Classificação em `status_rendimento`**:
  - `DIVULGADO`: Taxa numérica calculada e publicada pelo Censo Escolar;
  - `SEM_INFORMACAO_OU_NAO_OFERTADO`: Etapa não ofertada pela escola naquele ano letivo;
  - `FORA_DA_POPULACAO_HISTORICA`: Escola não existente ou não operante no período do Censo;
  - `SEM_INFORMACAO_ANO_FUTURO_OU_NAO_PUBLICADO`: Anos posteriores a 2023 (2024, 2025, 2026).
