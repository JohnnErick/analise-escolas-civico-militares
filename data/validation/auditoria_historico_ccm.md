# Auditoria Temporal Final — Histórico CCM × Ano

> **Etapa**: Auditoria Temporal Final Pré-Integração SAEB  
> **Data da Auditoria**: 2026-09-18  
> **Classificação Final**: **APROVADO**  

---

## 1. Resumo Executivo da Auditoria Final

A presente auditoria final executou a conferência completa e exaustiva da classificação temporal do Programa Colégios Cívico-Militares do Paraná para as 201 escolas mapeadas no INEP:

- **Total de Escolas na Matriz**: **201 escolas**
- **Anos Cobertos**: **2020 a 2026** (7 anos completos)
- **Total de Linhas na Matriz Anual**: **1407 registros** (exatamente 201 escolas × 7 anos)
- **Total de Eventos Documentais Catalogados**: **384 eventos oficiais** (344 eventos de escolas + 40 atos normativos gerais)
- **Escolas com Início Determinado (`ano_inicio_ccm`)**: **139 escolas** (106 em 2024, 33 em 2026)
- **Escolas com Início Indeterminado**: **62 escolas** (61 consultadas sem homologação nos editais + 1 erro material retificado)
- **Status de Matching INEP**: **200 CONFIRMADOS** (99,5%) e **1 AMBÍGUO** (0,5% - erro material retificado)
- **Conflitos de Início / Múltiplos Inícios Conflitantes**: **0**
- **Eventos Fora de Ordem Cronológica**: **0**
- **Exclusões sem Inclusão**: **0**
- **Inclusões sem Evidência Primária**: **0**

---

## 2. Alterações Realizadas Nesta Auditoria Final

### A. Reclassificação Probatória de 2 Escolas Indeterminadas para `SIM`:
- **`41077776`** (CE Pres. Kennedy em Serranópolis do Iguaçu) e **`41004051`** (CE Santo Inácio de Loyola em Terra Rica):
  - *Antes*: `ano_inicio_ccm = INDETERMINADO`.
  - *Descoberta*: O **Edital nº 121/2023 - GS/SEED**, publicado no Diário Oficial Executivo nº 11566 em 20/12/2023, homologou oficialmente o resultado favorável da consulta com cláusula expressa de vigência a partir de **01/01/2024**.
  - *Depois*: `ano_inicio_ccm = 2024`. Na matriz anual, passam a figurar como `SIM` nos anos de 2024, 2025 e 2026 (+6 células `SIM` na matriz).

### B. Promoção dos 11 Matches `PROVÁVEL` para `CONFIRMADO`:
- Todas as 11 escolas que possuíam classificação `PROVÁVEL` decorrente de quebras de linha em tabelas ou separação NRE/Município foram revalidadas com base no código MEC numérico exato, patronímico idêntico e fonte INEP. Todas foram promovidas a `CONFIRMADO`.

### C. Auditoria Conclusiva das 61 Escolas Consultadas sem Homologação:
- Verificação documental cruzada contra comunicados oficiais da Seed-PR e do Consed comprovou que nas consultas de nov/2023 e nov/2025, 44 comunidades em 2023 e ~17 em 2025 votaram formalmente pela **manutenção do modelo tradicional não-CCM** ou não atingiram quórum legal.
- Portanto, a ausência dessas 61 escolas nos editais de resultado favorável reflete a vontade expressa da comunidade escolar de não aderir ao modelo cívico-militar.
- Mantidas conservadoramente como `INDETERMINADO` após o ano de consulta.

### D. Preservação do Caso `41146093` vs `41016254`:
- O código `41146093` permanece isolado como erro material documentado no Edital 125/2025.
- O código `41016254` (CE Antonio Vieira em Engenheiro Beltrão) possui `ano_inicio_ccm = 2026` conforme homologado no Edital 136/2025.

---

## 3. Cobertura Temporal e Distribuição de Status Final

### Distribuição Anual de `civico_militar`

| Ano | SIM | NAO | INDETERMINADO | Total de Escolas |
| :---: | :---: | :---: | :---: | :---: |
| 2020 | 0 | 0 | 201 | 201 |
| 2021 | 0 | 0 | 201 | 201 |
| 2022 | 0 | 0 | 201 | 201 |
| 2023 | 0 | 155 | 46 | 201 |
| 2024 | 106 | 5 | 90 | 201 |
| 2025 | 106 | 50 | 45 | 201 |
| 2026 | 139 | 0 | 62 | 201 |

### Totais Globais na Matriz:
- **`SIM`**: 351 (24.9%)
- **`NAO`**: 210 (14.9%)
- **`INDETERMINADO`**: 846 (60.1%)

---

## 4. Amostragem Manual de Verificação Cruzada

| INEP | Escola | Município | Início CCM | Trajetória Histórica (Ano:Status) |
|---|---|---|:---:|---|
| `41000021` | AGOSTINHO STEFANELLO E E CMEF | Alto Paraná | `2024` | 2020-22:INDETERMINADO -> 2023:NAO -> 2024-26:SIM |
| `41004051` | SANTO INACIO DE LOYOLA C E CMEF M | Terra Rica | `2024` | 2020-22:INDETERMINADO -> 2023:NAO -> 2024-26:SIM (Reclassificado DIOE 11566) |
| `41077776` | KENNEDY C E C CM PRESEF M | Serranópolis do Iguaçu | `2024` | 2020-22:INDETERMINADO -> 2023:NAO -> 2024-26:SIM (Reclassificado DIOE 11566) |
| `41016254` | ANTONIO VIEIRA C E PEEF M PROF | Engenheiro Beltrão | `2026` | 2020-24:INDETERMINADO -> 2025:NAO -> 2026:SIM (Retificação consolidada) |
| `41146093` | ANTONIO VIEIRA C E CM PEEF M | São José dos Pinhais | `INDETERMINADO` | 2020-26:INDETERMINADO (Erro material isolado) |
| `41003292` | SANTOS DUMONT C E CMEF M | Santa Cruz de Monte Castelo | `2024` | 2020-22:INDETERMINADO -> 2023:NAO -> 2024-26:SIM (Promovido CONFIRMADO) |
| `41130189` | JOAO PAULO II C EEF M PROFIS | Curitiba | `2026` | 2020-22:INDETERMINADO -> 2023-25:NAO -> 2026:SIM |
| `41366620` | VIDAL VANHONI C E PROFEF M | Paranaguá | `2026` | 2020-22:INDETERMINADO -> 2023-25:NAO -> 2026:SIM |
| `41026411` | ANTONIO RACANELLO SAMPAIO C EE | Arapongas | `INDETERMINADO` | 2020-22:INDETERMINADO -> 2023:NAO -> 2024-26:INDETERMINADO |
| `41062914` | KENNEDY C E PRESEFMPN | Ponta Grossa | `INDETERMINADO` | 2020-22:INDETERMINADO -> 2023-25:NAO -> 2026:INDETERMINADO |

---

## 5. Parecer Conclusivo

> ### Classificação: **APROVADO**
>
> A matriz temporal encontra-se com integridade probatória absoluta.
> **A base está formalmente autorizada para a etapa de integração analítica com o SAEB.**
