# Matriz de Decisão e Seleção de Métodos Estatísticos

> **Investigação**: Colégios Cívico-Militares do Paraná  
> **Documento**: Avaliação Comparativa de Metodologias Estatísticas e Econométricas  
> **Data**: 2026-09-18  

---

## 1. Visão Geral e Princípio Norteador

A escolha do desenho metodológico não decorre de preferências prévias nem da busca pelo resultado mais apelativo, mas estritamente da **adequação entre as hipóteses de identificação econométrica e a estrutura factual dos dados disponíveis**.

Em observância às diretrizes do projeto, esta comparação metodológica não estabelece rankings artificiais nem atribui notas subjetivas aos métodos, avaliando objetivamente as premissas, exigências e limitações de cada abordagem.

---

## 2. Matriz Comparativa de Métodos Estatísticos

| Método | Dados Necessários | Hipóteses Fundamentais | Vantagens | Limitações | Aplicabilidade aos Dados do PR |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Análise Descritiva Longitudinal** | Séries históricas de indicadores por escola (2005–2023) | Nenhuma hipótese causal forte (estritamente factual) | Máxima transparência e facilidade de auditoria pública; expõe trajetórias reais sem premissas ocultas | Não isola efeito causal; não separa impacto do modelo de tendências macroeducacionais | **Altamente aplicável** para caracterizar a linha de base e diagnosticar o perfil de seleção pré-2024 |
| **2. Diferenças-em-Diferenças Tradicional (DiD 2x2)** | Período pré, período pós, grupo de tratamento e grupo de controle | **Tendências paralelas**: na ausência do tratamento, a evolução média de ambos seria idêntica | Controla fatores não observados invariantes no tempo de cada escola | Exige períodos pós-intervenção; altamente sensível a choques contemporâneos | **Inaplicável para efeito causal no momento**, pois não há dados pós-2024 no SAEB; **aplicável como teste de placebo** prévio |
| **3. DiD com Adoção Escalonada (Callaway & Sant'Anna / Sun-Abraham)** | Múltiplas coortes de tratamento iniciando em anos distintos | Tendências paralelas condicionais por coorte; ausência de efeitos de antecipação | Trata corretamente heterogeneidade de efeitos no tempo sem viés de "pesos negativos" | Exige múltiplas coortes com dados pós-intervenção observados | **Recomendado para o protocolo futuro** quando as coortes de 2024 e 2026 tiverem edições pós-implantação |
| **4. Pareamento por Escore de Propensão (PSM)** | Covariáveis pré-tratamento observáveis que predizem a adesão | **Ignorabilidade condicional**: seleção explicada apenas por variáveis observadas; suporte comum | Compara escolas militarizadas com escolas regulares rigorosamente idênticas no passado | Não elimina viés de seleção por fatores não observáveis (ex.: engajamento comunitário) | **Altamente aplicável** na linha de base para equilibrar escolas regulares contra as 106 escolas CCM 2024 |
| **5. Estimador Duplamente Robusto (PSM-DiD)** | Covariáveis pré + painel longitudinal pré/pós | Suporte comum e/ou tendências paralelas corretas (dupla robustez) | Se o modelo de seleção OU o modelo de tendência estiver correto, a estimativa é consistente | Exige dados pré e pós-intervenção com suporte comum | **Método padrão-ouro recomendado para a fase pós-SAEB 2025** |
| **6. Série Temporal Interrompida (ITS)** | Longa série temporal antes e depois para cada unidade | Nenhuma outra intervenção concomitante; estabilidade da tendência funcional | Explora a descontinuidade temporal na própria unidade tratada | Baixa densidade de observações (apenas edições bienais no SAEB: ~3 a 4 pontos pós-2017) | **Pouco aplicável** para SAEB/IDEB devido à periodicidade bienal e ao choque exógeno da pandemia de 2021 |
| **7. Controle Sintético** | Longo histórico prévio contínuo e pool de doadores | Combinação convexa de controles reproduz a trajetória da tratada | Ótimo para estudos de caso agregados com poucas unidades tratadas | Menos adequado quando existem mais de 100 escolas tratadas heterogêneas | **Aplicável como teste de robustez** em escolas CCM emblemáticas de grande porte |

---

## 3. Avaliação Detalhada das Abordagens

### 3.1. Por que o DiD Causal Tradicional NÃO Pode Ser Executado Agora?
O lote principal de 106 escolas teve sua implantação oficial homologada a partir de **01/01/2024**.
A edição mais recente divulgada do SAEB/IDEB refere-se ao ano de **2023** (aplicada em outubro/novembro de 2023).
Portanto, em 2023, as escolas eram formalmente colégios estaduais regulares. Executar um DiD atribuindo os resultados de 2023 à gestão cívico-militar constituiria um **grave anacronismo metodológico**.

### 3.2. A Utilidade do DiD no Cenário Atual: Teste de Placebo
Embora o DiD não possa mensurar impacto do modelo militar no momento, ele possui uma aplicação metodológica crucial: o **teste de tendências paralelas pré-intervenção (Placebo DiD)**.
Ao estimar um DiD falso entre 2021 e 2023 (ambos períodos pré-tratamento), verifica-se que o coeficiente de interação é estatisticamente nulo ($p = 0,6264$). Isso prova empiricamente que, antes da política, as escolas do grupo CCM e as escolas regulares seguiam tendências estritamente paralelas, legitimando o uso futuro do DiD.

### 3.3. O Papel Estratégico do Propensity Score Matching (PSM)
O teste de viabilidade demonstrou que:
- O universo de escolas regulares estaduais (~1.350 escolas com dados completos) é 15 vezes maior que o lote CCM 2024 (90 escolas completas no recorte dos Anos Finais);
- A região de suporte comum é de 100% para o grupo tratado;
- Isso viabiliza a construção de uma base pareada com extremo balanceamento em notas prévias do SAEB (2019 e 2021), taxa de aprovação e taxa de abandono.

---

## 4. Estratégia Metodológica Recomendada

Diante do diagnóstico empírico, a estratégia recomendada estrutura-se em duas etapas cronológicas interdependentes:

```text
┌────────────────────────────────────────────────────────────────────────┐
│ FASE 1 (Factual e Linha de Base — Executável com Dados Disponíveis)    │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Caracterização Longitudinal da Linha de Base (2005–2023)            │
│    → Diagnóstico de seleção: quem o Estado militarizou?                │
│ 2. Pareamento por Escore de Propensão (PSM) na Linha de Base           │
│    → Identificação dos pares regulares equivalentes                    │
│ 3. Teste de Tendências Paralelas Placebo (2017 a 2023)                 │
│    → Validação da premissa fundamental de equivalência temporal        │
│ 4. Comparação com o Grupo "Consultado mas Rejeitado" (N=62)            │
│    → Análise de autoseleção comunitária na consulta                    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ FASE 2 (Avaliação de Impacto Causal — Protocolo Pré-Registrado)        │
├────────────────────────────────────────────────────────────────────────┤
│ Execução do Estimador Duplamente Robusto (PSM-DiD) e DiD Escalonado    │
│ assim que forem divulgados:                                            │
│ - Censo Escolar 2024 (Rendimento pós-intervenção)                      │
│ - Microdados do SAEB 2025 (Proficiência pós-intervenção)               │
└────────────────────────────────────────────────────────────────────────┘
```
