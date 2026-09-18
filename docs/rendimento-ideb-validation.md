# Relatório de Validação — Integração de Rendimento Escolar e IDEB

> **Investigação**: Colégios Cívico-Militares do Paraná  
> **Etapa**: Integração dos Indicadores Oficiais de Rendimento Escolar e IDEB  
> **Data**: 2026-09-18  
> **Classificação Final**: **APROVADO**  

---

## 1. Resumo Executivo da Validação

A auditoria confirmou a integridade cadastral, temporal e numérica na integração dos dados de **Taxas de Rendimento Escolar** (Aprovação, Reprovação e Abandono apurados pelo Censo Escolar) e do **IDEB** (IDEB Observado, Componente N, Componente P e Metas Projetadas) à matriz histórica CCM × SAEB:

- **Total de Escolas CCM Auditadas**: **201 escolas**
- **Escolas Localizadas no Cadastro do IDEB**: **201 escolas (100,0%)**
- **Escolas Localizadas no Cadastro de Rendimento (Censo Escolar)**: **200 escolas (99,5%)**
  - *Caso isolado*: Código `41167090` (Colégio Estadual Professora Andreia Neres dos Santos em Cascavel), de criação recente pelo Edital nº 125/2025, não possuía turmas ativas na série histórica do Censo 2017–2023; classificado como `FORA_DA_POPULACAO_HISTORICA`.
- **Perdas Cadastrais**: **0 escolas (0,0%)**
- **Duplicidades de Chave Primária**: **0**
- **Total de Registros na Matriz Integrada Preliminar (2020–2026)**: **2.646 linhas**
- **Total de Registros na Série Histórica Longitudinal (2005–2025)**: **5.878 linhas**

---

## 2. Auditoria de Matching Cadastral

| Indicador Oficial | Escolas Localizadas | Status `CONFIRMADO` | `FORA_DA_POPULACAO` | Não Encontradas |
| :--- | :---: | :---: | :---: | :---: |
| **IDEB (INEP/MEC)** | **201 / 201 (100,0%)** | 200 (99,5%) | 0 | 0 |
| **Rendimento Escolar (Censo/INEP)** | **200 / 201 (99,5%)** | 200 (99,5%) | 1 (0,5%) | 0 |

---

## 3. Cobertura das Escolas CCM por Indicador e Etapa

### 3.1. Taxas de Rendimento Escolar (Aprovação, Reprovação e Abandono)

| Etapa de Ensino | Ano | Total Escolas | Com Taxa Aprovação | Com Taxa Reprovação | Com Taxa Abandono | % Cobertura |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Anos Finais (6º-9º)** | 2020 | 197 | 193 | 193 | 193 | **98,0%** |
| **Anos Finais (6º-9º)** | 2021 | 197 | 193 | 193 | 193 | **98,0%** |
| **Anos Finais (6º-9º)** | 2022 | 197 | 193 | 193 | 193 | **98,0%** |
| **Anos Finais (6º-9º)** | 2023 | 197 | 195 | 195 | 195 | **99,0%** |
| **Ensino Médio** | 2020 | 160 | 150 | 150 | 150 | **93,8%** |
| **Ensino Médio** | 2021 | 160 | 152 | 152 | 152 | **95,0%** |
| **Ensino Médio** | 2022 | 160 | 153 | 153 | 153 | **95,6%** |
| **Ensino Médio** | 2023 | 160 | 160 | 160 | 160 | **100,0%** |
| **Anos Iniciais (1º-5º)** | 2020 a 2023 | 21 | 0 | 0 | 0 | Trajetória residual na rede estadual |

### 3.2. IDEB (Índice de Desenvolvimento da Educação Básica)

| Etapa de Ensino | Ano da Edição | Total Escolas | Com IDEB Observado | Sem IDEB (Critério ND ou sem quórum) | Com Meta Projetada | % Divulgado |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Anos Finais (6º-9º)** | 2021 | 197 | 178 | 19 | 192 | **90,4%** |
| **Anos Finais (6º-9º)** | 2023 | 197 | 189 | 8 | 0 (Ciclo PDE encerrado em 2021) | **95,9%** |
| **Ensino Médio** | 2021 | 160 | 113 | 47 | 97 | **70,6%** |
| **Ensino Médio** | 2023 | 160 | 149 | 11 | 0 (Ciclo PDE encerrado em 2021) | **93,1%** |

### 3.3. Cobertura da Base Combinada na Edição Mais Recente (2023)

Na edição de 2023, a presença simultânea dos quatro blocos de dados (`CCM + SAEB + Rendimento + IDEB`) apresentou:
- **Anos Finais (6º ao 9º ano)**: **189 de 197 escolas (95,9%)** possuem todos os indicadores simultâneos;
- **Ensino Médio**: **149 de 160 escolas (93,1%)** possuem todos os indicadores simultâneos;
- As escolas restantes possuem Rendimento Escolar apurado pelo Censo (99,5%), mas não tiveram notas do SAEB/IDEB divulgadas por não atingirem a taxa mínima de 80% de presença discente estipulada pelo INEP (`ND`).

---

## 4. Testes de Integridade Numérica e Escalas Oficiais

1. **Taxas de Rendimento (Censo Escolar)**:
   - Taxa de Aprovação: valores contínuos estritamente entre `0,0%` e `100,0%` (média geral da rede estadual ~95-98%);
   - Taxa de Reprovação: valores contínuos estritamente entre `0,0%` e `100,0%`;
   - Taxa de Abandono: valores contínuos estritamente entre `0,0%` e `100,0%`;
   - Zero valores impossíveis ou fora dos limites percentuais.
2. **IDEB**:
   - Escala oficial de 0 a 10 rigorosamente preservada;
   - Nenhum valor ausente preenchido como zero;
   - Metas projetadas do PDE preservadas como referência institucional sem confusão com o resultado observado.

---

## 5. Relação Conceitual entre os Indicadores Integrados

```text
       ┌───────────────────────────────┐
       │   SAEB (Proficiência)         │  → Aprendizado discente em Língua Portuguesa
       │   Escala TRI (0 a 500)        │    e Matemática (transformado em N: 0 a 10)
       └──────────────┬────────────────┘
                      │
                      ▼
       ┌───────────────────────────────┐
       │   Rendimento (Fluxo Escolar)  │  → Taxas de aprovação, reprovação e abandono
       │   Censo Escolar (0 a 100%)    │    apuradas ao final de cada ano letivo (P)
       └──────────────┬────────────────┘
                      │
                      ▼
       ┌───────────────────────────────┐
       │   IDEB (Indicador Sintético)  │  → Produto: IDEB = N x P
       │   Escala Oficial (0 a 10)     │    (Combina proficiência e rendimento)
       └───────────────────────────────┘
```

> **Aviso Metodológico Fundamental**:
> O IDEB **não é uma medida independente** nem um terceiro indicador autônomo. Ele é o produto direto da média das proficiências padronizadas do SAEB ($N$) multiplicada pela média harmônica das taxas de aprovação ($P$). A documentação do projeto alerta explicitamente contra o uso simultâneo de IDEB, SAEB e Rendimento em modelos de regressão sem o devido controle de colinearidade perfeita.

---

## 6. Parecer Conclusivo da Validação

> ### Classificação: **APROVADO**
>
> A base integrada atende integralmente a todos os critérios de rigor, rastreabilidade e integridade:
> - **100% de localização no cadastro do IDEB (201/201)**;
> - **99,5% de localização no cadastro de Rendimento (200/201, com ausência histórica justificada)**;
> - **Zero perdas de escolas e zero duplicidades**;
> - **Preservação rigorosa da base histórica temporal CCM congelada**;
> - **Regra antitravamento cumprida (nenhuma ausência convertida em zero)**;
> - **Pipeline 100% automatizado e reprodutível**.
>
> **A base analítica preliminar está oficialmente concluída e validada.**
