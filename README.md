# 🏫 Painel de Análise: Escolas Cívico-Militares (Paraná)

Ambiente interativo de dados desenvolvido para suporte a investigações jornalísticas e análises educacionais sobre o desempenho de escolas públicas cívico-militares e não cívico-militares no Paraná.

---

## 🎯 Objetivo e Princípio Analítico

O objetivo deste projeto é fornecer uma **ferramenta de exploração e consumo de microdados** para jornalistas e analistas, permitindo investigar com rigor e transparência o desempenho dos estabelecimentos de ensino com base nas avaliações oficiais do **SAEB** e **IDEB**.

> **Nota de Neutralidade**: O painel não assume que escolas cívico-militares apresentem desempenho superior ou inferior. Seu papel é viabilizar a formulação de hipóteses, a observação de distribuições (e não apenas médias) e a contextualização territorial e histórica. Decisões causais e reportagens finais caberão às etapas posteriores da equipe investigativa.

---

## 📊 Estrutura dos Dados e Indicadores

Os dados foram consolidados a partir das planilhas oficiais fornecidas:
1. `planilha ref/divulgacao_pr_consolidado.xlsx`: Dados do **INEP / MEC** (IDEB e SAEB) para as 3 etapas de ensino no Paraná.
2. `planilha ref/Escolas civico militares.xlsx`: Relação oficial das **escolas cívico-militares** do Paraná (SEED-PR).

### Indicadores e Cobertura:
1. **Indicador Principal — SAEB**:
   - **Proficiência em Língua Portuguesa**: Escala do SAEB (~150 a 400 pontos);
   - **Proficiência em Matemática**: Escala do SAEB (~150 a 400 pontos);
   - **Nota Média Padronizada**: Escala de 0 a 10 calculada pelo INEP ($N$).

2. **Indicadores Complementares**:
   - **IDEB Observado**: Índice de Desenvolvimento da Educação Básica ($IDEB = N \times P$);
   - **Metas Projetadas**: Metas oficiais estabelecidas pelo MEC;
   - **Taxa de Aprovação (%) e Indicador de Rendimento ($P$)**: Fluxo escolar dos estudantes.
   - *Nota de Transparência*: A base original fornecida não contempla taxas explícitas de reprovação e abandono escolar.

3. **Cobertura Temporal e Espacial**:
   - **Unidade Federativa**: Paraná (PR);
   - **Período**: 2005 a 2025 (séries bianuais);
   - **Etapas de Ensino**: Anos Iniciais do EF (2.976 escolas), Anos Finais do EF (1.965 escolas) e Ensino Médio (1.704 escolas). Total de 4.941 estabelecimentos únicos.
   - **Escolas Cívico-Militares Mapeadas**: 322 em Anos Finais, 293 no Ensino Médio e 48 em Anos Iniciais.


---

## 🏷️ Regra de Classificação de Escolas

Conforme documentado no código (`preprocess_data.py`), a classificação adota as nomenclaturas oficiais da SEED-PR e INEP:
- **Cívico-Militar**: Escolas contendo no nome oficial as siglas `C E CM` (Colégio Estadual Cívico-Militar), `E E CM`, `E M CM`, `E C M`, `CPM` (Colégio da Polícia Militar), ou as expressões `CIVICO-MILITAR` / `MILITAR`.
- **Exclusão Específica**: Foram excluídos expressamente registros contendo `CMEI` / `C M E I` (Centros Municipais de Educação Infantil).
- **Não Cívico-Militar**: Todas as demais escolas da base.

---

## 🚀 Como Executar o Painel

### 1. Pré-requisitos
- Python 3.10 ou superior

### 2. Ativar Ambiente e Instalar Dependências
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Processar / Atualizar Dados (opcional, já processados)
```bash
python3 preprocess_data.py
```

### 4. Iniciar o Painel Streamlit
```bash
streamlit run app.py
```
O painel abrirá automaticamente no navegador no endereço `http://localhost:8501`.

---

## 📁 Estrutura de Arquivos

```text
analise-escolas/
├── app.py                     # Aplicação Streamlit principal
├── preprocess_data.py         # Pipeline de pré-processamento e padronização Parquet
├── requirements.txt           # Dependências do projeto
├── README.md                  # Documentação completa
├── data/                      # Arquivos estruturados em formato Parquet
│   ├── escolas_tidy.parquet   # Base consolidada em formato long (62.871 linhas)
│   ├── escolas_wide_*.parquet # Bases abertas por etapa
├── modules/                   # Módulos da aplicação
│   ├── data_loader.py         # Leitura em cache e filtros dinâmicos
│   ├── charts.py              # Visualizações em Plotly
│   ├── components.py          # KPIs, cards e tabelas
│   ├── views_saeb.py          # Módulo do indicador principal (SAEB)
│   ├── views_temporal.py      # Módulo de evolução histórica (2005-2025)
│   ├── views_complementary.py # Módulo de IDEB e Aprovação
│   ├── views_geo.py           # Módulo de comparação municipal
│   ├── views_explorer.py      # Microdados, ficha individual e exportação CSV
│   └── views_methodology.py   # Dicionário de dados e notas metodológicas
└── planilha ref/              # Planilha original consolidada
    └── divulgacao_pr_consolidado.xlsx
```
