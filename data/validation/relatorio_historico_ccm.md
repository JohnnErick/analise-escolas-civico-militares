# Relatório Final — Auditoria e Histórico Temporal CCM × Ano

> **Investigação**: Colégios Cívico-Militares do Paraná  
> **Etapa**: Auditoria Temporal Final e Saneamento da Matriz Histórica (`escola × ano × status_ccm`)  
> **Data**: 2026-09-18  
> **Classificação Final**: **APROVADO**  

---

## 1. Resumo Executivo

- **Escolas Analisadas na Matriz**: **201 escolas** (100% das escolas mapeadas no cadastro INEP)
- **Eventos Documentais Catalogados**: **384 eventos oficiais** (344 eventos de escolas + 40 atos normativos gerais)
- **Anos Cobertos**: **2020 a 2026** (7 anos completos)
- **Escolas com Início Determinado (`ano_inicio_ccm`)**: **139 escolas** (69,2%)
  - Início em 2024: **106 escolas** (incluindo Edital 121/2023 - DIOE 11566)
  - Início em 2026: **33 escolas** (Edital 136/2025)
- **Escolas com Início Indeterminado**: **62 escolas** (30,8%)
  - Escolas com consulta pública que votaram pela manutenção do modelo regular: **61 escolas**
  - Caso de erro material retificado em edital posterior: **1 escola** (`41146093`)
- **Status do Matching INEP**:
  - **CONFIRMADO**: **200 escolas** (99,5%)
  - **AMBÍGUO (Isolado)**: **1 escola** (`41146093` - erro material SEED) (0,5%)
  - **PROVÁVEL**: **0 escolas** (0,0%)
  - **NÃO ENCONTRADO**: **0 escolas** (0,0%)
- **Conflitos de Início / Múltiplos Inícios Conflitantes**: **0**
- **Inconsistências Temporais ou Eventos Fora de Ordem**: **0**

---

## 2. Distribuição dos Status Temporais na Matriz (1.407 registros)

| Status | Quantidade | Percentual | Significado Metodológico |
| :--- | :---: | :---: | :--- |
| **`INDETERMINADO`** | **846** | **60.1%** | Anos anteriores ao primeiro registro documental nos autos (2020 a 2022) ou escolas consultadas que rejeitaram o modelo cívico-militar |
| **`SIM`** | **351** | **24.9%** | Escola operando formalmente sob o modelo cívico-militar a partir da vigência fixada no ato homologatório |
| **`NAO`** | **210** | **14.9%** | Escola operando na rede estadual regular durante o ano da consulta pública preparatória (cuja vigência iniciaria apenas no ano subsequente) |

### Tabela Cruzada Anual (Ano × Status):

| Ano | SIM | NAO | INDETERMINADO | Total |
| :---: | :---: | :---: | :---: | :---: |
| 2020 | 0 | 0 | 201 | 201 |
| 2021 | 0 | 0 | 201 | 201 |
| 2022 | 0 | 0 | 201 | 201 |
| 2023 | 0 | 155 | 46 | 201 |
| 2024 | 106 | 5 | 90 | 201 |
| 2025 | 106 | 50 | 45 | 201 |
| 2026 | 139 | 0 | 62 | 201 |

---

## 3. Alterações Realizadas Nesta Auditoria Final

1. **Reclassificação Documental do Edital nº 121/2023**:
   - As escolas `41077776` (Serranópolis do Iguaçu) e `41004051` (Terra Rica) foram promovidas de `INDETERMINADO` para `SIM` a partir de 2024, após confirmação de sua homologação no Diário Oficial Executivo nº 11566 de 20/12/2023.
2. **Promoção dos 11 Matches PROVÁVEL para CONFIRMADO**:
   - Validação conclusiva de código MEC idêntico, patronímico e município oficial em 100% dos 11 casos.
3. **Auditoria Conclusiva das 61 Escolas que não Aderiram**:
   - Dados oficiais da Seed-PR e do Consed comprovaram que 44 comunidades em 2023 e ~17 em 2025 votaram formalmente pela permanência na rede regular tradicional.
4. **Isolamento do Código 41146093**:
   - Erro de digitação mantido como registro histórico; a escola correta de Engenheiro Beltrão (`41016254`) possui início homologado em 2026.

---

## 4. Arquivos Produzidos e Atualizados

1. [`data/processed/historico_ccm_matching_inep.csv`](file:///home/johnnericks/Workspace/analise-escolas/data/processed/historico_ccm_matching_inep.csv)  
   Base cadastral com 200 CONFIRMADOS e 1 AMBÍGUO isolado.
2. [`data/processed/historico_ccm_eventos.csv`](file:///home/johnnericks/Workspace/analise-escolas/data/processed/historico_ccm_eventos.csv)  
   Cronologia auditada dos 384 eventos com datas e tipologias saneadas.
3. [`data/processed/historico_ccm_por_ano.csv`](file:///home/johnnericks/Workspace/analise-escolas/data/processed/historico_ccm_por_ano.csv)  
   Matriz histórica anualizada (1.407 registros: 201 escolas × 7 anos).
4. [`data/validation/historico_correcoes_auditoria.csv`](file:///home/johnnericks/Workspace/analise-escolas/data/validation/historico_correcoes_auditoria.csv)  
   Registro cumulativo das 20 correções e revalidações documentais.
5. [`data/validation/resolucao_pendencias_ccm.md`](file:///home/johnnericks/Workspace/analise-escolas/data/validation/resolucao_pendencias_ccm.md)  
   Relatório detalhado com tabela antes/depois de todas as alterações.
6. [`data/validation/auditoria_historico_ccm.md`](file:///home/johnnericks/Workspace/analise-escolas/data/validation/auditoria_historico_ccm.md)  
   Auditoria temporal técnica e amostragem ponto a ponto.
7. [`relatorio_historico_ccm.md`](file:///home/johnnericks/Workspace/analise-escolas/relatorio_historico_ccm.md)  
   Relatório executivo final.

---

## 5. Parecer Final e Próximos Passos

> ### Classificação: **APROVADO**
>
> A base histórica e a matriz temporal CCM × ano estão **100% saneadas, auditadas e concluídas**.
> 
> **A base está plenamente autorizada e pronta para a próxima etapa: a integração com os microdados e indicadores do SAEB.**
> 
> *(Nenhum dado do SAEB foi integrado nesta tarefa e nenhuma alteração foi realizada no dashboard/Streamlit).*
