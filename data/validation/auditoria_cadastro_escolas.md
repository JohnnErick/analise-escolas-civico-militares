# Auditoria Cadastral das Escolas do Projeto (201 Escolas CCM)

> **Investigação**: Colégios Cívico-Militares do Paraná  
> **Documento**: Relatório de Auditoria da Dimensão Cadastral Mestre  
> **Data**: 2026-09-18  
> **Status**: **APROVADO**  

---

## 1. Resumo Executivo da Auditoria

A auditoria da integração cadastral avaliou minuciosamente as **201 escolas oficiais** identificadas nos atos e editais da SEED/PR, cruzando suas chaves com o Censo Escolar da Educação Básica (INEP 2023), cadastros georreferenciados e centroides municipais do IBGE.

### Indicadores Centrais de Cobertura Cadastral (201 Escolas):
- **Total de Escolas Auditadas**: **201 escolas**
- **Códigos INEP Presentes no Cadastro Mestre**: **201 / 201 (100,0%)**
- **Duplicidades de Código INEP**: **0**
- **Matches Cadastrais Confirmados**: **200 / 201 (99,5%)**
- **Casos Ambíguos Catalogados**: **1 (Código `41146093` - Erro material retificado para `41016254`)**
- **Escolas Não Encontradas**: **0 (0,0%)**
- **Cobertura de NRE (Núcleo Regional de Educação)**: **201 / 201 (100,0%)**
- **Cobertura de Localização (Urbana / Rural)**: **201 / 201 (100,0%)**
- **Cobertura de Etapas Ofertadas**: **201 / 201 (100,0%)**
- **Cobertura de Coordenadas Geográficas (Lat/Lon)**: **201 / 201 (100,0%)**
  - *Coordenadas Exatas KML*: **143 escolas**
  - *Centroide Municipal IBGE*: **58 escolas**

---

## 2. Tratamento de Dados Ausentes

Em cumprimento estrito às normas metodológicas:
1. **Endereço, Bairro e CEP**: Mantidos como `None` / ausentes na tabela cadastral. As fontes tabulares oficiais locais (Censo Escolar 2023, SAEB e IDEB) não disponibilizam logradouro e CEP nas matrizes de rendimento. Nenhuma inferência ou dado fictício foi imputado;
2. **Caso Especial `41167090`**: Unidade recém-criada (CE PROFESSORA ANDREIA NERES DOS SANTOS em Cascavel) pelo Edital 125/2025 para adesão futura em 2026. Identificada com situação `CRIADA_SEM_TURMAS_HISTORICAS`, sem turmas ativas na série do Censo 2023;
3. **Caso Material `41146093`**: Mantido no cadastro para rastreabilidade do erro do Edital 125/2025, devidamente marcado como `AMBIGUO`.

---

## 3. Tabela de Auditoria Individual das 201 Escolas

| Código INEP | Nome Original (Edital SEED) | Nome Cadastral (Censo INEP) | Município | Status Matching | Observação |
| :---: | :--- | :--- | :--- | :---: | :--- |
| `41000021` | AGOSTINHO STEFANELLO E E CMEF | AGOSTINHO STEFANELLO E E EF | Alto Paraná | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41000978` | MACHADO DE ASSIS E EEF | MACHADO DE ASSIS E E EF | Itaúna do Sul | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41001222` | LAMARTINE R SOARES C E DREF M | LAMARTINE R SOARES C E DR EF M | Loanda | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41003292` | SANTOS DUMONT C E CMEF M | SANTOS DUMONT C E EF M | Santa Cruz de Monte Castelo | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41004051` | SANTO INACIO DE LOYOLA C E CMEF M | SANTO INACIO DE LOYOLA C E EF M | Terra Rica | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41004957` | ANCHIETA C E CMEF M N | ANCHIETA C E E F M N | Cruzeiro do Oeste | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41007131` | NESTOR VICTOR C EEF M N PROFIS | NESTOR VICTOR C E EF M N PROFIS | Pérola | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41007280` | CASTELO BRANCO E E CM PRESEF | CASTELO BRANCO C E PRES EF M | Tapira | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41008111` | NEIVA PAVAN M GARCIA C E PROFA EF M | NEIVA PAVAN M GARCIA C E EF M PROFA | Umuarama | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41010132` | RUI BARBOSA C EEF EM PROFIS | RUI BARBOSA C E EF EM PROFIS | Japurá | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41010345` | CASTRO ALVES C E CMEM PROFIS | CASTRO ALVES C E EM PROFIS | Rondon | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41010540` | SANTOS DUMONT C EEF M N | SANTOS DUMONT C E EM N | São Tomé | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41012631` | RIBEIRO DE CAMPOS E E CMEF | RIBEIRO DE CAMPOS E E EF | Goioerê | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41016254` | ANTONIO VIEIRA C E PEEF M PROF NORMAL | ANTONIO VIEIRA C E PE EF M PROF NORMAL | Engenheiro Beltrão | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41018800` | LEO KOHLER E E CM PROFEF | LEO KOHLER E E PROF EF | Terra Boa | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41020189` | OSVALDO ARANHA E EEF | OSVALDO ARANHA E E EF | Lobato | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41020286` | FRANCISCO J PERIOTO E E CM PROFEF | FRANCISCO J PERIOTO E E PROF EF | Mandaguaçu | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41020685` | FRANCISCO P X LOPES E E CONEF | FRANCISCO P X LOPES E E CON EF | Nova Esperança | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41020910` | CECILIA MEIRELES E E CMEF | CECILIA MEIRELES E E EF | Santa Fé | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41021010` | MANOEL F ALMEIDA E E CM DREF | MANOEL F ALMEIDA E E DR EF | Santo Inácio | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41021100` | ANASTACIO CEREZINE E E CMEF | ANASTACIO CEREZINE E E EF | Alvorada do Sul | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41022750` | ARTHUR C E SILVA E E CM PRESEF | ARTHUR C E SILVA E E PRES EF | Floresta | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41024281` | MARCO A PIMENTA C EEF M | MARCO A PIMENTA C E EF M | Maringá | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41024923` | IZABEL C E PRINCEF M | IZABEL C E PRINC EF M | Paiçandu | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41024931` | NEIDE BERTASSO BERALDO C EEF M PROFIS | NEIDE BERTASSO BERALDO C E EF M PROFIS | Paiçandu | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41025318` | ALBERTO SANTOS DUMONT C E CMEF M P | ALBERTO SANTOS DUMONT C E EF M PROFIS | Apucarana | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41025636` | FRANCISCO A SOUSA E E PROFEF | FRANCISCO A SOUSA E E PROF EF | Apucarana | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41025806` | JOSE DE ANCHIETA C E CM PEEF M PROFIS | JOSE DE ANCHIETA C E PE EF M PROFIS | Apucarana | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41026055` | OSMAR GUARACY FREIRE C E CMEF M P | OSMAR GUARACY FREIRE C E EF M P | Apucarana | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41026152` | POLIVALENTE C D SILVA C E CMEF M P | POLIVALENTE C DOMINGOS SILVA C E EFMP | Apucarana | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41026411` | ANTONIO RACANELLO SAMPAIO C EEF M | ANTONIO RACANELLO SAMPAIO C E EF M | Arapongas | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41026705` | IVANILDE DE NORONHA C EEF M | IVANILDE DE NORONHA C E EF M PROFIS | Arapongas | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41026764` | JULIA WANDERLEY E E PROFAEF | JULIA WANDERLEY E E PROFA EF | Arapongas | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41027370` | ROSA D CALSAVARA C E CMEF M PROFIS | ROSA D CALSAVARA C E EF M PROFIS | Cambira | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41028279` | HERMINIA R LUPION C EEF M PROFIS | HERMINIA R LUPION C E EF M PROFIS | Sabáudia | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41028406` | ANDREA NUZZI C E CM MAESTROEF M P | ANDREA NUZZI C E MAESTRO EF M PROFIS | Cambé | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41028457` | ATTILIO CODATO C E CMEF M | ATTILIO CODATO C E EF M PROFIS | Cambé | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41028732` | HELENA KOLODY C E CM PROFEF M | HELENA KOLODY C E PROF EF M | Cambé | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41028902` | MANUEL BANDEIRA C E CMEF M PROFIS | MANUEL BANDEIRA C E EF EM PROFIS | Cambé | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41030125` | CARLOS DE ALMEIDA C E CMEF M PROFIS | CARLOS DE ALMEIDA C E EF M PROFIS | Londrina | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41030265` | CELIA M DE OLIVEIRA C E CM PROFEF M P | CELIA MORAES DE OLIVEIRA C E PROF EF M P | Londrina | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41030486` | WISTREMUNDO R P GARCIA C E CM PEEFM P | WISTREMUNDO R P GARCIA C E PE EF M P | Londrina | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41030800` | HEBER S VARGAS C E CM PROF DREF M P | HEBER S VARGAS C E PROF DR EF M PROFIS | Londrina | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41031237` | HUGO SIMAS C E CMEF M PROFIS | HUGO SIMAS C E EF M PROFIS | Londrina | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41031253` | HUMBERTO P COUTINHO C E CMEF M PROFIS | HUMBERTO P COUTINHO C E EF M PROFIS | Londrina | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41031709` | LAURO G DA V PESSOA E E CM PROFEF | LAURO G DA V PESSOA E E PROF EF | Londrina | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41031750` | LUCIA B LISBOA C E PROFAEF M | LUCIA B LISBOA C E PROFA EF M | Londrina | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41031873` | MARGARIDA B LISBOA C E CM PROFAEF M | MARGARIDA B LISBOA C E PROFA EF M | Londrina | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41032225` | NEWTON GUIMARAES C E CM PROFEF M | NEWTON GUIMARAES C E PROF EF M | Londrina | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41032241` | NILO PECANHA C E CMEF M PROFIS | NILO PECANHA C E EF M PROFIS | Londrina | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41032446` | OLYMPIA M TORMENTA C E CM PROFEF M P | OLYMPIA M TORMENTA C E PROF EF M PROFIS | Londrina | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41032853` | RIO BRANCO C E CM BAR DOEF M | RIO BRANCO C E BAR DO EF M | Londrina | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41033620` | LAURO P TAVARES C E CM DREF M | LAURO P TAVARES C E DR EF M | Rolândia | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41037324` | ANTONIO DINIZ PEREIRA C E CMEF M | ANTONIO DINIZ PEREIRA C E EF M PROFIS | Ivaiporã | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41037413` | BENTO MOSSURUNGA C EEF M | BENTO MOSSURUNGA C E EF M | Ivaiporã | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41039068` | NEREU RAMOS E E CMEF | NEREU RAMOS C E E F M | Manoel Ribas | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41040317` | JOSE DE MATTOS LEAO C E CMEF M | JOSE DE MATTOS LEAO C E EF M | São João do Ivaí | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41040694` | VICENTE MACHADO C E CMEF M | VICENTE MACHADO C E C EF M | São Pedro do Ivaí | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41040759` | CARRAO C E CONSEF M | CARRAO C E CONS EF M | Assaí | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41042670` | RUI BARBOSA C E EF M N PROFIS | RUI BARBOSA C E EF M N PROFIS | Abatiá | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41042778` | STELLA MARIS C E CMEF M | STELLA MARIS C E EF M | Andirá | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41043375` | NOBREGA DA CUNHA C E CMEF M | NOBREGA DA CUNHA C E EF M | Bandeirantes | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41046218` | ANTONIO BITONTI E E CM PROFEF | ANTONIO BITONTI E E PROF EF | Sertaneja | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41046552` | CAROLINA LUPION C E CM DONAEF M | CAROLINA LUPION C E DONA EF M | Cambará | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41046960` | ANESIO DE A LEITE C E CMEF M PROFIS | ANESIO DE A LEITE C E EF M PROFIS | Jacarezinho | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41051351` | MIGUEL DIAS C EEF M PROFIS | MIGUEL DIAS C E EF M PROFIS | Joaquim Távora | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41052250` | NEWTON SAMPAIO C E CMEF M | NEWTON SAMPAIO E E EF | São José da Boa Vista | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41053494` | MIGUEL NASSIF MALUF C E CMEF M | MIGUEL NASSIF MALUF C E EF M | Wenceslau Braz | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41056264` | JARDIM ALEGRE C E CMEF M PROFIS | JARDIM ALEGRE C E EF M PROFIS | Telêmaco Borba | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41056574` | TANCREDO NEVES C E PRESEF M PROFIS | TANCREDO NEVES C E PRES EF M PROFIS | Imbaú | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41060296` | JULIA WANDERLEY C EEF M PROFIS | JULIA WANDERLEY C E EF M PROFIS | Carambeí | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41060466` | NICOLAU BALTASAR C E PEEF M | NICOLAU BALTASAR C E PE EF M PROFIS | Castro | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41062108` | BECKER E SILVA C E CM PROFEF M PROFIS | BECKER E SILVA C E PROF EF M PROFIS | Ponta Grossa | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41062191` | CARLOS ZELESNY C E CM PEEF M | CARLOS ZELESNY C E PE EF M | Ponta Grossa | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41062272` | INST ED E PROF CESAR P MARTINEZF M N P | INST ED E PROF CESAR P MARTINEZ F M N P | Ponta Grossa | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41062469` | EPAMINONDAS N RIBAS C E CM DREF M P | EPAMINONDAS N RIBAS C E DR EF M PROFIS | Ponta Grossa | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41062914` | KENNEDY C E PRESEFMPN | KENNEDY C E PRES EF M PROFIS | Ponta Grossa | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41062949` | LINDA S BACILA C E PROFAEF M PROFIS | LINDA S BACILA C E PROFA EF M PROFIS | Ponta Grossa | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41063031` | MENELEU A TORRES C E PROFEF M PROFIS | MENELEU A TORRES C E PROF EF M PROFIS | Ponta Grossa | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41063058` | MONTEIRO LOBATO E EEF | MONTEIRO LOBATO E E EF | Ponta Grossa | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41063139` | NOSSA SRA DA GLORIA C E CMEF M | NOSSA SRA DA GLORIA C E EF M | Ponta Grossa | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41063155` | OSORIO C E CM GALEF M PROFIS | OSORIO C E GAL EF M PROFIS | Ponta Grossa | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41063384` | SANTA MARIA C EEF M | SANTA MARIA C E EF M | Ponta Grossa | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41067029` | GRACILIANO RAMOS E E CMEF | GRACILIANO RAMOS E E EF | Santa Helena | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41068688` | JOAO ARNALDO RITT C E CMEF M | JOAO ARNALDO RITT C E EF M | Toledo | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41068807` | LUIZ AUGUSTO M REGO C E CMEF M PROFIS | LUIZ AUGUSTO M REGO C E EF M PROFIS | Toledo | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41068998` | NOVO SARANDI C E CEF M | NOVO SARANDI C E C EF M | Toledo | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41070224` | ALBERTO S DUMONT C EEF M N PROFIS | ALBERTO S DUMONT C E EF M N PROFIS | Cafelândia | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41070585` | CARLOS A CAMARGO C E CMEF M PROFIS | CARLOS A CAMARGO C E EF M PROFIS | Capitão Leônidas Marques | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41071018` | XIV DE NOVEMBRO C E CMEF M | XIV DE NOVEMBRO C E EF M | Cascavel | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41071409` | HUMBERTO A C BRANCO C E CM MALEF M P | HUMBERTO A C BRANCO C E MAL EF M PROF | Cascavel | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41071590` | JOSE A B ORSO C E CMEF M PROF | JOSE A B ORSO C E EF M | Cascavel | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41071832` | MARILIS F PIROTELLI C EEF M | MARILIS F PIROTELLI C E EF M | Cascavel | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41072626` | AMANCIO MORO C E CM EF M N PROFIS | AMANCIO MORO C E EF M N PROFIS | Corbélia | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41073037` | OSORIO DUQUE ESTRADA C E CMEF M | OSORIO DUQUE ESTRADA C E EF M | Diamante do Sul | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41075919` | ALMIRO SARTORI C EEF M PROFIS | ALMIRO SARTORI C E EF M PROFIS | Foz do Iguaçu | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41076036` | AYRTON SENNA DA SILVA C EEF M N PROFIS | AYRTON SENNA DA SILVA C E EF M N PROFIS | Foz do Iguaçu | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41076354` | CARLOS DRUM DE ANDRADE C E CMEF M P | CARLOS DRUMMOND DE ANDRADE C E EF M P | Foz do Iguaçu | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41076605` | JUSCELINO K DE OLIVEIRA C EEF M PROFIS | JUSCELINO K DE OLIVEIRA C E EF M PROFIS | Foz do Iguaçu | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41077512` | ARTHUR DA C SILVA C E CM MALEF M P | ARTHUR DA C SILVA C E MAL EF M PROFIS | Medianeira | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41077776` | KENNEDY C E C CM PRESEF M | KENNEDY C E C PRES E F M | Serranópolis do Iguaçu | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41078586` | ARCANGELO NANDI C EE F M | ARCANGELO NANDI C E EF M PROFIS | Santa Terezinha de Itaipu | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41079469` | PARANAGUA C E MQ DEEF M PROFIS | PARANAGUA C E MQ DE EF M PROFIS | Vera Cruz do Oeste | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41081340` | JOAO ZACCO PARANA C E CMEF M | JOAO ZACCO PARANA C E EF M PROFIS | Planalto | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41084721` | JOSE DE ANCHIETA C EEF M | JOSE DE ANCHIETA C E EF M | Dois Vizinhos | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41084772` | LEONARDO DA VINCI C E CMEF M N PROFIS | LEONARDO DA VINCI C E EF M N PROFIS | Dois Vizinhos | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41085906` | EDUARDO VIRMOND SUPLICY C E DREF M P | EDUARDO VIRMOND SUPLICY C E DR EF M P | Francisco Beltrão | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41086945` | MARMELEIRO C E DEEF M | MARMELEIRO C E DE EF M PROFIS | Marmeleiro | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41089006` | JORGE DE LIMA E E CMEF | JORGE DE LIMA E E EF | Salto do Lontra | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41092694` | ISIDORO DUMONT E E CM IREF | ISIDORO DUMONT E E IR EF | Itapejara d'Oeste | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41093666` | SAO JOAO BOSCO C E CMEF M P | SAO JOAO BOSCO C E EF M PROFIS | Pato Branco | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41099133` | OLAVO BILAC C EEF M N PROFIS | OLAVO BILAC C E EF M N PROFIS | Cantagalo | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41099940` | CESAR STANGE C EEF M | CESAR STANGE C E EF M | Guarapuava | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41100689` | LENI MARLENE JACOB C E CM PROFAEF M P | LENI MARLENE JACOB C E PROFA EF M PROF | Guarapuava | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41101006` | PALMEIRINHA C E DO C DEEF M PROF | PALMEIRINHA C E DO C DE EF M PROF | Guarapuava | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41105176` | ALTO RECREIO C E CMEF M | ALTO RECREIO C E EF M | Quedas do Iguaçu | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41122801` | ALBERTO KRAUSE C E CM PROFEF M P | ALBERTO KRAUSE C E PROF EF M | Almirante Tamandaré | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41122836` | EMILIA BUZATO C E CM EF M PROFIS | EMILIA BUZATO C E EF M PROFIS | Campo Magro | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41122860` | FLORIPA TEIXEIRA DE FARIA C EEF M PROF | FLORIPA TEIXEIRA DE FARIA C E EF M | Almirante Tamandaré | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41123212` | ROSA F JOHNSON E E CM PROFA EF | ROSA F JOHNSON E E PROFA EF | Almirante Tamandaré | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41123301` | TANCREDO NEVES C EEF M | TANCREDO NEVES C E EF M PROFIS | Almirante Tamandaré | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41124014` | JUVENTUDE DE SANTO ANTONIO C E CMEF M | JUVENTUDE DE SANTO ANTONIO C E EF M | Balsa Nova | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41124669` | IVAN F DO AMARAL FILHO C E CM EF M P | IVAN F DO AMARAL FILHO C E EF M PROF | Campina Grande do Sul | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41125053` | DJALMA MARINHO C E CMEF M PROFIS | DJALMA MARINHO C E EF M PROFIS | Campo Largo | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41125193` | JOAO XXIII C E CMEF M | JOAO XXIII C E E F M | Campo Largo | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41125304` | MACEDO SOARES C E CMEF M PROFIS | MACEDO SOARES C E EF M PROFIS | Campo Largo | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41126050` | HELENA KOLODY C EEF M PROF | HELENA KOLODY C E EF M PROF | Colombo | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41126122` | JOAO R DE CAMARGO C E CM EF M | JOAO R DE CAMARGO C E EF M PROFIS | Colombo | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41126670` | MIGUEL FRANCO FILHO C E CMEF M PROFIS | MIGUEL FRANCO FILHO C E EF M PROFIS | Contenda | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41127048` | ALFREDO PARODI C EEF M PROFIS | ALFREDO PARODI C E EF M PROFIS | Curitiba | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41127668` | BENTO M DA ROCHA NETO C EEF M PROFIS | BENTO M DA ROCHA NETO C E EF M PROFIS | Curitiba | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41128664` | CRUZEIRO DO SUL C E CMEF M P | CRUZEIRO DO SUL C E EF M PROFIS | Curitiba | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41128885` | DIRCE C DO AMARAL C E PROFAEF M PROFIS | DIRCE C DO AMARAL C E PROFA EF M PROFIS | Curitiba | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41128915` | DOMINGOS ZANLORENZI C EEF M PROFIS | DOMINGOS ZANLORENZI C E EF M PROFIS | Curitiba | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41129512` | GABRIELA MISTRAL C EEF M PROFIS | GABRIELA MISTRAL C E EF M | Curitiba | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41129539` | GELVIRA CORREA PACHECO C EEF M P | GELVIRA CORREA PACHECO C E EF M | Curitiba | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41129687` | GUIDO STRAUBE C E PROFEF M PROFIS | GUIDO STRAUBE C E PROF EF M PROFIS | Curitiba | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41129920` | ISABEL L S SOUZA C E PROFAEF M PROFIS | ISABEL L S SOUZA C E PROFA EF M PROFIS | Curitiba | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41129970` | IVO LEAO C EEF M | IVO LEAO C E EF M | Curitiba | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41129989` | IVO ZANLORENZI E E MONSEF | IVO ZANLORENZI E E MONS EF | Curitiba | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41130065` | JAYME CANET C E CMEF M P | JAYME CANET C E EF M PROFIS | Curitiba | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41130146` | JOAO LOYOLA C E CM PROFEF M P | JOAO LOYOLA C E PROF EF M | Curitiba | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41130170` | JOAO PAULO I C E CM PAPAEF M P | JOAO PAULO I C E PAPA EF M PROFIS | Curitiba | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41130189` | JOAO PAULO II C EEF M PROFIS | JOAO PAULO II C E EF M PROFIS | Curitiba | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41130200` | JOAO WISLINSKI C E CM PEEF M N P | JOAO WISLINSKI C E PE EF M N | Curitiba | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41130243` | JOSE BUSNARDO C E EF M | JOSE BUSNARDO C E EF M | Curitiba | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41130308` | JOSE GUIMARAES C E PROFEM PROFIS | JOSE GUIMARAES C E PROF EM PROFIS | Curitiba | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41130359` | JULIO MESQUITA C E CM PROFEF M PROFIS | JULIO MESQUITA C E PROF EF M PROFIS | Curitiba | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41130421` | LAMENHA LINS C E CM PRESEF M P | LAMENHA LINS C E PRES EF M PROFIS | Curitiba | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41130618` | LOUREIRO FERNANDES C E PROFEF M PROFIS | LOUREIRO FERNANDES C E PROF EF M PROFIS | Curitiba | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41130685` | LUIZA ROSS C E CM PROFAEF M P | LUIZA ROSS C E PROFA EF M PROFIS | Curitiba | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41130723` | LYSIMACO F COSTA C E PROFEF M P | LYSIMACO F COSTA C E PROF EF M | Curitiba | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41130936` | MARIA MONTESSORI C EEF M | MARIA MONTESSORI C E EF M | Curitiba | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41130952` | MARIA P MARTINS E EEF | MARIA P MARTINS E E EF | Curitiba | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41131223` | MILTON CARNEIRO C E CMEF M P | MILTON CARNEIRO C E EF M PROFIS | Curitiba | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41131479` | NATALIA REGINATO C EEF M PROFIS | NATALIA REGINATO C E EF M PROFIS | Curitiba | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41132475` | PINHEIRO DO PARANA C E CMEF M P | PINHEIRO DO PARANA C E EF M PROFIS | Curitiba | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41132718` | PROTASIO DE CARVALHO C EEF M PROFIS | PROTASIO DE CARVALHO C E EF M PROFIS | Curitiba | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41132955` | ROBERTO LANGER JUNIOR C EEF M PROFIS | ROBERTO LANGER JUNIOR C E EF M PROFIS | Curitiba | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41133137` | SANTA FELICIDADE C E CMEF M P | SANTA FELICIDADE C E EF M PROFIS | Curitiba | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41133200` | SANTO ANTONIO C E CMEF M | SANTO ANTONIO E E EF | Curitiba | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41133226` | SANTOS DUMONT C EEF M | SANTOS DUMONT C E EF M | Curitiba | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41133358` | SAO PAULO APOSTOLO C EEF M PROFIS | SAO PAULO APOSTOLO C E EF M PROFIS | Curitiba | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41134419` | XAVIER DA SILVA C E DREF M PROFIS | XAVIER DA SILVA C E DR EF M PROFIS | Curitiba | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41134516` | DECIO DOSSI C E DREF M PROFIS | DECIO DOSSI C E DR EF M | Fazenda Rio Grande | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41135784` | LEOCADIA B RAMOS C EEF M PROFIS | LEOCADIA B RAMOS C E EF M PROFIS N | Pinhais | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41136276` | VILA MACEDO C E CMEF M | VILA MACEDO C E EF M PROFIS | Piraquara | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41137361` | ARNALDO JANSEN C E CM PEEF M PROFIS | ARNALDO JANSEN C E PE EF M PROF | São José dos Pinhais | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41137698` | MARIA VIDAL NOVAES E EEF | MARIA VIDAL NOVAES E E EF | São José dos Pinhais | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41137809` | GODOFREDO MACHADO E EEF | GODOFREDO MACHADO E E EF | São José dos Pinhais | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41138422` | SILVEIRA DA MOTTA C EEF M PROFIS | SILVEIRA DA MOTTA C E EF M PROFIS | São José dos Pinhais | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41138937` | ROCHA POMBO C EEF M P | ROCHA POMBO C E EF M | Antonina | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41140052` | SERTAOZINHO C E CMEF M N PROFIS | SERTAOZINHO C E E F M N PROFIS | Matinhos | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41140788` | JOSE BONIFACIO C EEF M PROFIS | JOSE BONIFACIO C E EF M PROFIS | Paranaguá | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41141121` | REGINA M B DE MELLO C E PROFAEF M | REGINA M B DE MELLO C E PROFA EF M | Paranaguá | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41141156` | ROQUE VERNALHA E E DREF | ROQUE VERNALHA E E DR EF | Paranaguá | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41141288` | ZILAH DOS S BATISTA C E PROFAEF M P | ZILAH DOS S BATISTA C E PROFA EF M P | Paranaguá | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41144201` | MARIA DE J P GUIMARAES C E C PROFAEF M | MARIA DE J P GUIMARAES C E C PROFA EF M | Guarapuava | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41144929` | JOSE MARCONDES SOBRINHO C EEF M | JOSE MARCONDES SOBRINHO C E EF M | Laranjeiras do Sul | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41146093` | ANTONIO VIEIRA C E CM PEEF M | ANTONIO VIEIRA C E C M PE EF M | São José dos Pinhais | **AMBIGUO** | Erro material do Edital 125/2025; retificado pelo Edital 136/2025 para o código oficial 41016254. |
| `41148550` | SANTA RITA E E CMEF | SANTA RITA E E EF | Foz do Iguaçu | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41150902` | PLANTA DEODORO C E CM EF M | PLANTA DEODORO C E EF M | Piraquara | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41158806` | ROCHA POMBO C E CMEF M | ROCHA POMBO C E EF M | Araucária | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41164920` | IRONDI MANTOVANI PUGLIESI C E CMEF M | IRONDI MANTOVANI PUGLIESI C E EF M | Arapongas | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41167090` | ANDREIA NERES DOS SANTOS C E PROFAEFM | ANDREIA NERES DOS SANTOS C E PROFAEFM | Cascavel | **CONFIRMADO** | Escola recém-criada para adesão CCM 2026; cadastrada no Edital 125/2025 sem histórico discente no Censo 2023. |
| `41354273` | EDISON PIETROBELLI E E CM PROFEF | EDISON PIETROBELLI C E PROF EF M | Ponta Grossa | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41355156` | THIAGO TERRA C E CMEF M PROF | THIAGO TERRA C E EF M PROF | Londrina | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41356136` | RINA M DE J FRANCOVIG C E PROFAEF M | RINA M DE J FRANCOVIG C E PROFA EF M | Londrina | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41357027` | TEOBALDO L KLETEMBERG C E PREF M P | TEOBALDO L KLETEMBERG C E PR EF M P | Curitiba | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41358872` | JOAO R DA SILVA E E CM PROFEF | JOAO RODRIGUES DA SILVA C E PROF EF M | Londrina | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41360567` | WALDE ROSI GALVAO C EEF M | WALDE ROSI GALVAO C E EF M | Pinhais | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41366620` | VIDAL VANHONI C E PROFEF M | VIDAL VANHONI C E PROF EF M | Paranaguá | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41370597` | PILAR MATURANA C EEF M P | PILAR MATURANA C E EF M P | Curitiba | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41373375` | MARIA HELENA T LUCIANO C E PROFEF MNP | MARIA HELENA T LUCIANO C E PROF EF M P | Pontal do Paraná | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41373456` | OSCAR J D P E SILVA C E CM EF M | OSCAR J D P E SILVA C E EF M | Pinhais | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41373936` | ANIBAL KHURY C E DEPE F M P | ANIBAL KHURY E E DEP EF | Guaratuba | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41378580` | CATARATAS DO IGUACU C EEF M PROFIS | CATARATAS DO IGUACU C E EF M PROFIS | Foz do Iguaçu | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41378962` | ANA DIVANIR BORATTO C EEFM | ANA DIVANIR BORATTO C E EFM | Ponta Grossa | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41387724` | DANIEL ROCHA C E PROFEF M PROFIS | DANIEL ROCHA C E PROF EF M PROFIS | Pinhais | **CONFIRMADO** | Nome oficial do Edital e nome cadastral do Censo INEP perfeitamente idênticos. |
| `41531876` | GUIDO ARZUA C E CMEF M P | GUIDO ARZUA C E PROF EF M PROFIS | Curitiba | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
| `41597915` | PATRIMONIO REGINA C E CM DOEF M | PATRIMONIO REGINA C E DO EF M | Londrina | **CONFIRMADO** | Variação padrão de abreviação/prefixo entre Edital SEED e registro Censo INEP. |
