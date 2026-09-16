# 🏫 Painel de Análise: Escolas Cívico-Militares do Paraná

Ambiente interativo de exploração de dados educacionais (SAEB e IDEB) para jornalismo investigativo e análise de políticas públicas no Estado do Paraná.

---

## 🍎 Como Usar no MacBook (1 Duplo Clique — Sem Programação)

Este projeto foi preparado para que **qualquer pessoa sem conhecimento técnico** consiga abrir o painel em menos de 2 minutos.

> [!TIP]
> **Os dados já vão 100% embutidos no projeto** (`data/escolas_tidy.parquet` com apenas 1,5 MB). Você **não precisa** baixar arquivos adicionais, nem ter Excel instalado, nem rodar scripts de tratamento.

### Passo a Passo no Mac:
1. **Baixe o projeto**: Faça o clone pelo Git ou baixe a pasta compactada (ZIP) no botão verde `Code` do GitHub e extraia no seu MacBook.
2. **Abra a pasta no Finder**.
3. Dê um **duplo clique no arquivo `iniciar_painel.command`**.

**O que vai acontecer automaticamente:**
- O script detecta o Python do seu Mac;
- Na primeira vez, ele prepara o ambiente silenciosamente (leva cerca de 1 minuto);
- **O seu navegador de internet padrão (Safari ou Chrome) abrirá automaticamente** exibindo o painel interativo em `http://localhost:8501`.
- Para encerrar o painel no final do dia, basta fechar a janelinha preta do Terminal.

---

## 🪟 Como Usar no Windows (1 Duplo Clique)
Caso utilize Windows, basta dar **duplo clique no arquivo `iniciar_painel.bat`**. O navegador abrirá automaticamente.

---

## ☁️ Alternativa em Nuvem: Acesso Direto pela Web (Sem Instalar Nada)
Se preferir compartilhar o painel com outros colegas de redação ou leitores sem que eles precisem baixar nada no computador:
1. Conecte este repositório no [Streamlit Community Cloud](https://share.streamlit.io/) (gratuito).
2. Clique em **Deploy**.
3. O painel ficará acessível via link web (ex: `https://seu-usuario-analise-escolas.streamlit.app`) pelo navegador de qualquer computador ou celular.

---

## 💻 Para Desenvolvedores (Linha de Comando)

Se desejar executar manualmente pelo terminal:

```bash
# 1. Criar e ativar o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# 2. Instalar as dependências
pip install -r requirements.txt

# 3. Executar o painel
streamlit run app.py
```

Para atualizar o matching geoespacial ou reprocessar os microdados a partir das planilhas brutas:
```bash
python3 scripts/spatial_matching_kml.py
python3 preprocess_data.py
python3 gerar_planilha_cruzada.py
```

---

## 📊 Estrutura dos Dados e Metodologia

- **Universo de Cobertura**: 4.941 estabelecimentos de ensino no Paraná avaliados pelo INEP/MEC entre **2005 e 2025**.
- **Georreferenciamento de 100% dos Colégios Cívico-Militares**: Todos os 306 colégios cívico-militares oficiais da SEED-PR foram validados com coordenadas de Latitude e Longitude a partir do arquivo KML oficial, eliminando 100% das ambiguidades de homônimos.
- **Indicador Principal**: Proficiências do SAEB (Matemática, Língua Portuguesa e Nota Média Padronizada de 0 a 10).
- **Indicadores Complementares**: IDEB Observado, Metas Projetadas do MEC e Taxas de Aprovação / Rendimento Escolar.
- **Mapa Geoespacial Interativo**: Aba de comparação municipal com mapa de pontos do Paraná por etapa de ensino.
- **Exportação Disponível**: Botões para download de microdados em CSV e da planilha consolidada completa em Excel `.xlsx`.

---

## 📁 Arquitetura de Pastas

```text
analise-escolas/
├── iniciar_painel.command    # 🚀 Inicializador de 1 clique para macOS (MacBook)
├── iniciar_painel.sh         # Inicializador shell para Linux/Mac via terminal
├── iniciar_painel.bat        # Inicializador de 1 clique para Windows
├── app.py                   # Ponto de entrada da aplicação Streamlit
├── requirements.txt         # Pacotes Python necessários
├── README.md                # Guia de uso e documentação
├── .streamlit/
│   └── config.toml          # Configuração silenciosa do Streamlit (sem telemetria)
├── data/                    # 📦 DADOS EMBUTIDOS (Leves e prontos para uso)
│   ├── escolas_tidy.parquet # Base analítica consolidada (62.871 linhas, 1.5 MB)
│   ├── base_parana_cruzada_completa.xlsx # Planilha consolidada com abas e Lat/Lon (3.9 MB)
│   ├── mapeamento_escolas_civico_militares.csv # 306 colégios mapeados (Lat/Lon/INEP)
│   └── municipios_pr.csv    # Coordenadas oficiais dos 399 municípios do PR
├── modules/                 # Módulos modulares do painel
│   ├── data_loader.py       # Carregamento e filtros com cache
│   ├── charts.py            # Visualizações Plotly e mapa interativo
│   ├── components.py        # KPIs, cartões métricos e tabelas
│   ├── views_saeb.py        # Aba SAEB (Principal)
│   ├── views_temporal.py    # Aba Séries Históricas
│   ├── views_complementary.py # Aba IDEB & Rendimento
│   ├── views_geo.py         # Aba Comparativo Municipal e Mapa
│   ├── views_explorer.py    # Aba Explorador de Microdados e Ficha Individual
│   └── views_methodology.py # Aba Metodologia e Transparência
└── scripts/
    └── spatial_matching_kml.py # Algoritmo de matching geoespacial KML x INEP
```
