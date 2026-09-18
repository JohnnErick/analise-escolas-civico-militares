# Relatório de Validação — Integração Metodológica CCM × SAEB

> **Investigação**: Colégios Cívico-Militares do Paraná  
> **Etapa**: Validação e Auditoria da Integração dos Dados do SAEB/IDEB  
> **Data**: 2026-09-18  
> **Classificação Final**: **APROVADO**  

---

## 1. Resumo Executivo da Integridade

A auditoria de integração verificou a consistência cadastral, a cobertura das variáveis de proficiência e a ausência de distorções na junção entre a base histórica temporal CCM (2020–2026) e os dados oficiais do SAEB/IDEB divulgados pelo INEP:

- **Total de Escolas CCM Auditadas**: **201 escolas**
- **Total de Escolas Localizadas no Cadastro SAEB**: **201 escolas (100,0%)**
- **Escolas Perdidas no Cruzamento**: **0 escolas (0,0%)**
- **Duplicidades Cadastrais**: **0**
- **Total de Registros na Matriz Integrada (2020–2026 por Etapa)**: **2646 linhas**
- **Total de Registros na Série Histórica Longitudinal (2005–2025)**: **3198 linhas**

---

## 2. Auditoria do Matching Cadastral Escolar

| Status do Matching | Quantidade | Percentual | Descrição Metodológica |
| :--- | :---: | :---: | :--- |
| **`CONFIRMADO`** | **200** | **99.5%** | Código INEP/ID_ESCOLA exato, nome da escola e município concordantes no cadastro do INEP |
| **`AMBÍGUO`** | **1** | **0.5%** | Código `41146093` isolado como erro material da SEED (retificado para `41016254`) |
| **`NAO_ENCONTRADO`** | **0** | **0,0%** | Zero escolas não encontradas |
| **`REVISAR`** | **0** | **0,0%** | Zero pendências cadastrais |

---

## 3. Cobertura de Proficiência SAEB (Edições 2021 e 2023)

Nos anos de aplicação do SAEB compreendidos no período histórico da matriz (2021 e 2023), a presença e divulgação das proficiências médias em Matemática e Língua Portuguesa apresentaram o seguinte comportamento:

| Etapa de Ensino | Ano SAEB | Total de Escolas Ofertantes | Com Nota Matemática | Com Nota Português | Com IDEB | Não Divulgado (Critério INEP - ND) | Sem Participação (-) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Anos Finais (6º-9º) | 2021 | 197 | 178 (90.4%) | 178 (90.4%) | 178 | 14 | 5 |
| Anos Finais (6º-9º) | 2023 | 197 | 189 (95.9%) | 189 (95.9%) | 189 | 1 | 4 |
| Anos Iniciais (1º-5º) | 2021 | 21 | 0 (0.0%) | 0 (0.0%) | 0 | 0 | 21 |
| Anos Iniciais (1º-5º) | 2023 | 21 | 0 (0.0%) | 0 (0.0%) | 0 | 0 | 21 |
| Ensino Médio | 2021 | 160 | 113 (70.6%) | 113 (70.6%) | 113 | 37 | 10 |
| Ensino Médio | 2023 | 160 | 149 (93.1%) | 149 (93.1%) | 149 | 0 | 11 |

### Destaques de Cobertura:
- **Anos Finais do Ensino Fundamental (6º ao 9º ano)**:
  - Em 2023: **189 de 197 escolas (95,9%)** possuem proficiências oficiais válidas.
  - Em 2021: **178 de 197 escolas (90,4%)** possuem proficiências oficiais válidas.
- **Ensino Médio**:
  - Em 2023: **149 de 160 escolas (93,1%)** possuem notas oficiais válidas.
  - Em 2021: **113 de 160 escolas (70,6%)** possuem notas oficiais válidas.
- **Anos Iniciais (1º ao 5º ano)**:
  - 21 escolas ofertam a etapa na rede estadual, com histórico mantido para completude.

---

## 4. Consistência Cruzada (Status CCM × Disponibilidade SAEB)

A tabela abaixo documenta a distribuição das escolas conforme seu status institucional na época da aplicação do SAEB e a disponibilidade da avaliação:

| Ano da Edição | Status CCM na Matriz | Total de Observações | SAEB Disponível | SAEB Ausente / Não Divulgado | Interpretação Metodológica |
| :---: | :---: | :---: | :---: | :---: | :--- |
| 2021 | **INDETERMINADO** | 378 | 291 | 87 | Escola operando na rede regular antes do início do modelo; constitui dado de baseline / pré-intervenção. |
| 2023 | **INDETERMINADO** | 82 | 71 | 11 | Escola operando na rede regular antes do início do modelo; constitui dado de baseline / pré-intervenção. |
| 2023 | **NAO** | 296 | 267 | 29 | Escola operando na rede regular antes do início do modelo; constitui dado de baseline / pré-intervenção. |

> **Nota Fundamental de Investigação Jornalística**:
> Como o lote principal das 201 escolas CCM teve seu início oficial fixado em **2024** (106 escolas) e em **2026** (33 escolas), os resultados das edições do SAEB de **2021 e 2023** representam primariamente o **desempenho histórico prévio (baseline / pré-adesão)** das escolas enquanto operavam sob o regime regular tradicional da rede pública paranaense.
> Essa constatação é de valor inestimável para impedir conclusões anacrônicas que atribuam o desempenho de 2021 ou 2023 à gestão cívico-militar nessas unidades.

---

## 5. Tratamento de Ausências e Regras Antitravamento

1. **Ausência não é Zero**: Nenhuma ausência de proficiência foi imputada como zero ou nota fictícia. Valores ausentes permanecem como `NaN` numérico acompanhados da variável descritiva `STATUS_PARTICIPACAO_SAEB`.
2. **Diferenciação Formal de Ausência**:
   - `DIVULGADO`: Nota calculada e publicada oficialmente pelo INEP;
   - `NAO_DIVULGADO_CRITERIO_INEP` (`ND`): Escola participou da avaliação, porém não atingiu a taxa mínima de participação de 80% dos matriculados ou o mínimo de 10 estudantes presentes;
   - `SEM_PARTICIPACAO` (`-`): Escola não participou da edição ou etapa não ofertada no respectivo ano letivo;
   - `SEM_EDICAO_SAEB_ANO_PAR_OU_INTERMEDIARIO`: Anos em que não houve aplicação nacional da avaliação censitária do SAEB (anos pares: 2020, 2022, 2024, 2026).

---

## 6. Parecer Conclusivo da Validação

> ### Classificação: **APROVADO**
>
> A integração metodológica entre a base histórica CCM e os dados do SAEB/IDEB atende plenamente a todos os requisitos de rigor técnico, rastreabilidade e integridade:
> - **Zero perdas de escolas (100% de localização no INEP)**;
> - **Preservação integral do status CCM auditado**;
> - **Tratamento transparente de ausências e notas ND**;
> - **Série histórica longitudinal completa (2005–2025) e matriz do período (2020–2026) consolidadas**.
>
> **A base integrada está oficialmente validada e concluída.**
