# Dimensão Cadastral Mestre das Escolas (`escolas_cadastro`)

> **Investigação**: Colégios Cívico-Militares do Paraná  
> **Documento**: Especificação Técnica e Dicionário de Dados da Dimensão Cadastral  
> **Data**: 2026-09-18  
> **Status**: Auditado e Validado  

---

## 1. Visão Geral e Finalidade

A tabela cadastral mestre [`data/processed/escolas_cadastro.parquet`](file:///home/johnnericks/Workspace/analise-escolas/data/processed/escolas_cadastro.parquet) (e sua versão em texto delimitado [`escolas_cadastro.csv`](file:///home/johnnericks/Workspace/analise-escolas/data/processed/escolas_cadastro.csv)) consolida as características institucionais, geográficas e operacionais dos estabelecimentos de ensino da rede pública do Paraná.

A integração cadastral atua como a **dimensão mestra** do modelo estrela educacional do projeto:

```text
               ┌───────────────────────┐
               │    escolas_cadastro   │
               │   (Dimensão Mestre)   │
               └───────────┬───────────┘
                           │ codigo_inep
         ┌─────────────────┼─────────────────┬─────────────────┐
         │                 │                 │                 │
         ▼                 ▼                 ▼                 ▼
┌─────────────────┐┌────────────────┐┌────────────────┐┌────────────────┐
│  Histórico CCM  ││   Dados SAEB   ││   Rendimento   ││   Dados IDEB   │
│  (Fato Eventos) ││(Fato Desempenho││  (Fato Fluxo)  ││ (Fato Síntese) │
└─────────────────┘└────────────────┘└────────────────┘└────────────────┘
```

---

## 2. Princípios Norteadores de Construção

1. **Chave Primária Oficial**: O relacionamento é operado exclusivamente por `codigo_inep` (código de 8 dígitos atribuído pelo INEP/MEC). Não há matching primário por nome textual;
2. **Preservação de Dados Factuais**: Não foi alterado nenhum valor das bases históricas pré-existentes (`historico_ccm_por_ano.csv`, `saeb`, `rendimento`, `ideb`);
3. **Diferenciação entre Cadastro Atual e Histórico**:
   - As variáveis cadastrais operacionais refletem o ano-base do Censo Escolar 2023;
   - As variações de nomenclatura oficial ao longo do tempo foram preservadas através da coexistência das colunas `nome_escola` (registro censitário oficial) e `nome_original_edital` (denominação constante dos editais da SEED/PR);
4. **Política Rígida de Dados Ausentes**: Variáveis que não constam nas matrizes tabulares oficiais disponíveis localmente (como logradouro, bairro e CEP) são mantidas estritamente como `None` / ausentes, sendo vedada qualquer imputação ou preenchimento por inferência.

---

## 3. Dicionário de Dados de `escolas_cadastro`

| Coluna | Tipo | Descrição e Regra de Preenchimento | Exemplo / Domínio |
| :--- | :--- | :--- | :--- |
| `codigo_inep` | `Int64` | Código identificador único oficial da escola no MEC/INEP (Chave Primária) | `41025318` |
| `nome_escola` | `String` | Nome oficial do estabelecimento registrado no Censo Escolar 2023 | `ALBERTO SANTOS DUMONT C E EF M` |
| `municipio` | `String` | Nome oficial do município paranaense sede da escola | `Apucarana` |
| `codigo_ibge_municipio` | `Int64` | Código numérico de 7 dígitos do município padronizado pelo IBGE | `4101408` |
| `uf` | `String` | Unidade da Federação (`PR`) | `PR` |
| `nre` | `String` | Núcleo Regional de Educação da SEED/PR responsável pela jurisdição da unidade | `APUCARANA` |
| `endereco` | `String` | Endereço completo / logradouro (*mantido ausente por não constar nas bases locais*) | `None` |
| `bairro` | `String` | Bairro / localidade (*mantido ausente por não constar nas bases locais*) | `None` |
| `cep` | `String` | Código de Endereçamento Postal (*mantido ausente por não constar nas bases locais*) | `None` |
| `latitude` | `Float64` | Latitude geográfica (graus decimais) | `-23.5539536` |
| `longitude` | `Float64` | Longitude geográfica (graus decimais) | `-51.4679734` |
| `tipo_coordenada` | `String` | Procedência metodológica da coordenada: `EXATA_KML` ou `CENTROIDE_MUNICIPIO` | `EXATA_KML` |
| `dependencia_administrativa` | `String` | Esfera administrativa de vinculação institucional | `Estadual`, `Municipal`, `Federal`, `Privada` |
| `rede_ensino` | `String` | Classificação padronizada da rede educacional | `Pública Estadual`, `Pública Municipal`, etc. |
| `localizacao` | `String` | Zona de localização censitária do estabelecimento | `Urbana` ou `Rural` |
| `situacao_funcionamento` | `String` | Situação operacional da escola: `EM_ATIVIDADE` ou `CRIADA_SEM_TURMAS_HISTORICAS` | `EM_ATIVIDADE` |
| `etapas_ofertadas` | `String` | Etapas ativas apuradas no Censo Escolar | `Anos Finais (6º-9º), Ensino Médio` |
| `fonte` | `String` | Especificação detalhada das fontes primárias que alimentaram o registro | `INEP/Censo 2023, SEED-PR Editais, KML, IBGE` |
| `ano_referencia` | `String` | Ano de referência das informações cadastrais | `2023` |
| `is_ccm` | `Boolean` | Indicador se o estabelecimento integra as 201 escolas auditadas do programa CCM | `True` ou `False` |
| `ano_inicio_ccm` | `String` | Ano formal de início homologado ou status institucional no programa CCM | `2024`, `2026`, `INDETERMINADO` |
| `status_ccm_atual` | `String` | Status vigente do modelo na unidade escolar | `SIM`, `FUTURO_2026`, `INDETERMINADO`, `NAO_CCM` |
| `nome_original_edital` | `String` | Grafia literal da escola constante nos Editais da SEED/PR | `ALBERTO SANTOS DUMONT, C E-EF M PROFIS` |

---

## 4. Subdivisões e Arquivos Especializados

Para otimizar o fluxo de trabalho e permitir consultas diretas:
1. [`data/processed/escolas_cadastro.parquet`](file:///home/johnnericks/Workspace/analise-escolas/data/processed/escolas_cadastro.parquet): Arquivo colunar de alta performance contendo as **5.966 escolas** do Paraná (estaduais, municipais e privadas) ativas no Censo Escolar 2023 mais as unidades criadas;
2. [`data/processed/escolas_cadastro.csv`](file:///home/johnnericks/Workspace/analise-escolas/data/processed/escolas_cadastro.csv): Versão completa em formato CSV delimitado por ponto e vírgula (`sep=';'`);
3. [`data/processed/escolas_cadastro_ccm.csv`](file:///home/johnnericks/Workspace/analise-escolas/data/processed/escolas_cadastro_ccm.csv): Recorte especializado contendo **exclusivamente as 201 escolas CCM** auditadas pelo projeto;
4. [`data/processed/auditoria_cadastro_escolas.csv`](file:///home/johnnericks/Workspace/analise-escolas/data/processed/auditoria_cadastro_escolas.csv): Tabela individualizada de auditoria de matching para as 201 escolas.
