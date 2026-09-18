# Relatório de Validação da Integração Cadastral das Escolas

> **Investigação**: Colégios Cívico-Militares do Paraná  
> **Documento**: Relatório de Validação e Auditoria da Dimensão Cadastral  
> **Data**: 2026-09-18  
> **Status da Etapa**: **APROVADO**  
> **Script de Validação**: [`scripts/validation/validar_cadastro_escolas.py`](file:///home/johnnericks/Workspace/analise-escolas/scripts/validation/validar_cadastro_escolas.py)  

---

## 1. Resumo Executivo da Validação

A etapa de **Integração dos Dados Cadastrais das Escolas** foi concluída com sucesso e aprovada em todos os 12 testes formais de consistência cadastral, integridade referencial e auditoria relacional, obtendo a classificação final:

$$\mathbf{APROVADO}$$

O objetivo exclusivo desta etapa foi incorporar ao projeto uma dimensão cadastral padronizada, fidedigna e plenamente rastreável para as escolas paranaenses, com foco individualizado nas **201 escolas auditadas** do programa de Colégios Cívico-Militares (CCM).

Nenhuma inferência, imputação ou dado arbitrário foi introduzido. Todas as bases anteriores de histórico CCM, SAEB, Rendimento Escolar e IDEB foram verificadas e mantiveram-se **100% inalteradas e congeladas**.

---

## 2. Indicadores Centrais de Cobertura Cadastral (201 Escolas CCM)

```text
================================================================================
DIAGNÓSTICO DA AUDITORIA CADASTRAL DAS 201 ESCOLAS CCM
================================================================================
Métrica Cadastral                              Resultado Obtido       Taxa (%)
--------------------------------------------------------------------------------
Escolas CCM Auditadas no Projeto                  201 escolas          100,0%
Códigos INEP Localizados no Cadastro Mestre       201 / 201            100,0%
Duplicidades de Chave Primária (codigo_inep)        0 ocorrências        0,0%
Matches Cadastrais CONFIRMADOS                    200 / 201             99,5%
Casos Ambíguos Históricos Documentados              1 / 201              0,5%
Escolas sem Cadastro (Não Encontradas)              0 / 201              0,0%
--------------------------------------------------------------------------------
Cobertura de NRE (Núcleo Regional de Educação)    201 / 201            100,0%
Cobertura de Município e UF ('PR')                201 / 201            100,0%
Cobertura de Dependência Administrativa           201 / 201            100,0%
Cobertura de Rede de Ensino ('Pública Estadual')  201 / 201            100,0%
Cobertura de Localização (Urbana / Rural)         201 / 201            100,0%
Cobertura de Etapas Ofertadas                     201 / 201            100,0%
Cobertura de Coordenadas Geográficas (Lat/Lon)    201 / 201            100,0%
  - Ponto Georreferenciado Exato (KML)            103 escolas           51,2%
  - Centroide Municipal Sede (IBGE)                98 escolas           48,8%
--------------------------------------------------------------------------------
Endereço, Bairro e CEP Mantidos como Ausentes     201 / 201            100,0%
Bases Anteriores Congeladas e Inalteradas         Todas verificadas    100,0%
Integridade Relacional de Merge (JOIN 1:1)        Aprovada sem perdas  100,0%
================================================================================
```

---

## 3. Síntese dos 12 Testes Automatizados de Validação

Executados e atestados pelo script [`scripts/validation/validar_cadastro_escolas.py`](file:///home/johnnericks/Workspace/analise-escolas/scripts/validation/validar_cadastro_escolas.py):

1. **Unicidade de Chave Primária**: O campo `codigo_inep` em [`data/processed/escolas_cadastro.parquet`](file:///home/johnnericks/Workspace/analise-escolas/data/processed/escolas_cadastro.parquet) é estritamente único entre todas as 5.966 escolas paranaenses cadastradas (zero duplicidades);
2. **Cobertura Universal das 201 Escolas**: 100% dos códigos INEP oficiais identificados na base [`historico_ccm_por_ano.csv`](file:///home/johnnericks/Workspace/analise-escolas/data/processed/historico_ccm_por_ano.csv) estão presentes no cadastro mestre;
3. **Completude de NRE (Núcleo Regional de Educação)**: Todos os 201 estabelecimentos possuem seu respectivo NRE identificado diretamente dos Editais Oficiais da SEED/PR (ex.: Editais nº 101/2023, 107/2023, 121/2023, 125/2025 e 136/2025);
4. **Completude Geográfica Básica**: Município oficial e Unidade da Federação (`PR`) preenchidos em 100% das unidades;
5. **Completude Institucional**: 100% das escolas CCM possuem dependência administrativa classificada como `Estadual` e rede de ensino classificada como `Pública Estadual`;
6. **Classificação de Localização**: 199 escolas classificadas como `Urbana` e 2 escolas como `Rural` (CE CÍVICO-MILITAR DO CAMPO DE SÃO ROQUE e CE CÍVICO-MILITAR DO CAMPO MARQUÊS DE CARAVELAS), conforme apurado no Censo Escolar 2023;
7. **Integridade das Coordenadas**: Todas as 201 escolas contam com latitude e longitude válidas no intervalo territorial do Paraná, com rastreabilidade metodológica expressa em `tipo_coordenada` (`EXATA_KML` ou `CENTROIDE_MUNICIPIO`);
8. **Mapeamento de Etapas Ofertadas**: Etapas educacionais ativas categorizadas a partir dos registros de turmas do Censo Escolar (predominância de unidades ofertando concomitantemente Anos Finais do EF e Ensino Médio);
9. **Conformidade de Dados Ausentes**: Os campos `endereco`, `bairro` e `cep` são estritamente nulos (`None` / `NaN`), comprovando que nenhuma informação ausente nas fontes tabulares locais foi preenchida por inferência arbitrária;
10. **Validação da Tabela de Auditoria Individual**: A tabela [`data/processed/auditoria_cadastro_escolas.csv`](file:///home/johnnericks/Workspace/analise-escolas/data/processed/auditoria_cadastro_escolas.csv) contém as 201 escolas individualizadas, com 200 registros categorizados como `CONFIRMADO` e 1 como `AMBIGUO`;
11. **Invariância das Bases Anteriores**: Verificação direta das dimensões e esquemas de dados de todas as bases legadas do projeto, comprovando zero alterações estruturais ou numéricas;
12. **Integridade Relacional (JOIN)**: Teste determinístico de junção entre o cadastro mestre e as tabelas `historico_ccm_por_ano.csv` e `ccm_saeb_rendimento_ideb.parquet`, atestando 100% de correspondência das chaves estrangeiras sem geração de valores nulos indesejados.

---

## 4. Auditoria de Casos Especiais e Discrepâncias Cadastrais

### 4.1. Caso Histórico Ambíguo: Código `41146093`
- **Registro no Edital 125/2025**: Listado erroneamente como Colégio Estadual Padre Antônio Vieira em Engenheiro Beltrão com o código `41146093`.
- **Registro no Edital de Retificação 136/2025**: Corrigido formalmente pelo governo para o código `41016254`.
- **Tratamento no Cadastro**: O código `41146093` foi preservado com o status `AMBIGUO` e observação explícita de erro material do edital, mantendo o histórico factual íntegro e evitando que o código seja descartado silenciosamente.

### 4.2. Caso Especial de Unidade Recém-Criada: Código `41167090`
- **Identificação**: Colégio Estadual Professora Andreia Neres dos Santos, município de Cascavel, NRE Cascavel.
- **Origem Documental**: Criado e submetido à consulta pública pelo Edital 125/2025 e homologado pelo Edital 136/2025 para início do modelo CCM em **2026**.
- **Situação no Censo Escolar 2023**: Por ter sido criado formalmente no ciclo de 2025, não possuía turmas ativas na série histórica do Censo Escolar 2023.
- **Tratamento no Cadastro**: Incorporado com situação operacional `CRIADA_SEM_TURMAS_HISTORICAS` e coordenadas baseadas no centroide municipal de Cascavel, preenchendo todos os requisitos cadastrais institucionais.

### 4.3. Variações de Nomenclatura entre Editais e Censo INEP
A auditoria constatou que as diferenças entre `nome_original` (Edital SEED) e `nome_cadastral` (Censo INEP) restringem-se a variações padronizadas de abreviação e prefixação educacional (por exemplo: `C E-EF M` nos editais vs. `C E EF M` no Censo; ou uso de `PROF` vs. `PROFESSOR`). Todas as 200 escolas com status `CONFIRMADO` referem-se inequivocamente aos mesmos estabelecimentos físicos e institucionais.

---

## 5. Conclusão e Classificação

A base cadastral consolidada atende plenamente aos 10 requisitos estabelecidos, garantindo:
1. Rastreabilidade total das 201 escolas;
2. Ausência de inventabilidade de dados;
3. Preservação do histórico e de bases prévias congeladas;
4. Integração unívoca via código INEP.

Portanto, a etapa é formalmente classificada como:

$$\mathbf{APROVADO}$$
