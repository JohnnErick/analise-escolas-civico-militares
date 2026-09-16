"""
Gera a planilha Excel final consolidada resultante do cruzamento:
- 'planilha ref/Escolas civico militares.xlsx'
- 'planilha ref/divulgacao_pr_consolidado.xlsx' (filtrado rigorosamente para SG_UF == 'PR')
"""

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RELATORIO_PATH = BASE_DIR / "data" / "relatorio_cruzamento_escolas.csv"
PLANILHA_PR = BASE_DIR / "planilha ref" / "divulgacao_pr_consolidado.xlsx"
EXCEL_SAIDA = BASE_DIR / "data" / "base_parana_cruzada_completa.xlsx"

# 1. Carrega o mapeamento
df_map = pd.read_csv(RELATORIO_PATH, sep=";", encoding="utf-8-sig")
ids_cm = set(df_map["ID_ESCOLA"].dropna().astype(int).unique())

# 2. Carrega as abas da planilha do Paraná e adiciona colunas de cruzamento
xls = pd.ExcelFile(PLANILHA_PR)

with pd.ExcelWriter(EXCEL_SAIDA, engine="openpyxl") as writer:
    # Aba 1: Resumo Metodológico do Cruzamento
    df_resumo = pd.DataFrame([
        {"Item": "Unidade Federativa", "Detalhe": "Paraná (PR) — Filtro exclusivo para escolas do estado"},
        {"Item": "Fonte dos Dados Educacionais", "Detalhe": "INEP / MEC — divulgacao_pr_consolidado.xlsx"},
        {"Item": "Fonte da Lista Cívico-Militar", "Detalhe": "SEED-PR — escolas_civico_militares_pr-final.csv (305 estabelecimentos válidos)"},
        {"Item": "Total de Escolas Cívico-Militares Cruzadas", "Detalhe": f"{len(ids_cm)} escolas únicas no Paraná"},

        {"Item": "Total de Estabelecimentos Únicos no PR", "Detalhe": "4.941 escolas"},
        {"Item": "Critério de Cruzamento", "Detalhe": "Mapeamento determinístico e por correspondência de entidades (ID_ESCOLA INEP)"},
        {"Item": "Indicador Principal", "Detalhe": "SAEB (Proficiência Língua Portuguesa, Matemática e Nota Média 0-10)"},
        {"Item": "Indicadores Complementares", "Detalhe": "IDEB Observado, Projeção de Metas e Taxas de Aprovação"},
        {"Item": "Nota sobre Reprovação/Abandono", "Detalhe": "Não constam na base oficial de divulgação fornecida pelo INEP"},
    ])
    df_resumo.to_excel(writer, sheet_name="Resumo_Cruzamento", index=False)
    
    # Aba 2: Lista Mapeada das Escolas Cívico-Militares
    df_map_clean = df_map.rename(columns={
        "NOME_PLANILHA_CIVICO_MILITAR": "Nome na Lista Oficial (SEED-PR)",
        "ID_ESCOLA": "Código INEP (ID_ESCOLA)",
        "NO_ESCOLA_INEP": "Nome Oficial no INEP",
        "NO_MUNICIPIO": "Município",
        "REDE": "Rede de Ensino",
        "SG_UF": "UF",
        "SCORE_SIMILARIDADE": "Score de Similaridade",
        "STATUS_CRUZAMENTO": "Status do Cruzamento"
    })
    df_map_clean.to_excel(writer, sheet_name="Lista_Civico_Militares", index=False)
    
    # Abas 3, 4, 5: Dados por etapa com as colunas de cruzamento
    nomes_abas = {
        "divulgacao_anos_finais": "Anos_Finais_PR",
        "divulgacao_ensino_medio": "Ensino_Medio_PR",
        "divulgacao_anos_iniciais": "Anos_Iniciais_PR"
    }
    
    for aba_origem, aba_destino in nomes_abas.items():
        df_etapa = pd.read_excel(xls, sheet_name=aba_origem)
        # Filtro estrito: Paraná
        df_etapa = df_etapa[df_etapa["SG_UF"].astype(str).str.strip().str.upper() == "PR"].copy()
        
        # Insere a coluna de cruzamento logo após o nome da escola
        df_etapa["ESCOLA_CIVICO_MILITAR"] = df_etapa["ID_ESCOLA"].apply(
            lambda x: "Sim" if pd.notna(x) and int(x) in ids_cm else "Não"
        )
        df_etapa["ORIGEM_CLASSIFICACAO"] = df_etapa["ID_ESCOLA"].apply(
            lambda x: "Lista Oficial SEED-PR" if pd.notna(x) and int(x) in ids_cm else "Não Cívico-Militar"
        )
        
        # Reordena colunas para destacar a classificação do cruzamento
        cols = df_etapa.columns.tolist()
        pos_escola = cols.index("NO_ESCOLA") + 1
        cols.remove("ESCOLA_CIVICO_MILITAR")
        cols.remove("ORIGEM_CLASSIFICACAO")
        cols.insert(pos_escola, "ESCOLA_CIVICO_MILITAR")
        cols.insert(pos_escola + 1, "ORIGEM_CLASSIFICACAO")
        df_etapa = df_etapa[cols]
        
        df_etapa.to_excel(writer, sheet_name=aba_destino, index=False)
        print(f"Salva aba {aba_destino}: {len(df_etapa)} linhas.")

print(f"\nPlanilha consolidada completa gerada em: {EXCEL_SAIDA}")
