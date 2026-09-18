#!/usr/bin/env python3
"""
importar_rendimento_inep.py

Script para leitura, filtragem e importação dos microdados e tabelas oficiais
das Taxas de Rendimento Escolar (Aprovação, Reprovação e Abandono) divulgadas
pelo INEP/MEC a partir do Censo Escolar da Educação Básica (edições 2017 a 2023).

Filtra exclusivamente os estabelecimentos de ensino do Estado do Paraná (SG_UF == 'PR').

Fontes:
- data/raw/rendimento/tx_rend_escolas_{ano}.zip (2017 a 2023)

Saídas:
- data/raw/rendimento/rendimento_parana_raw.parquet
"""

import zipfile
from pathlib import Path
import pandas as pd

def run():
    print("=== Iniciando Importação das Taxas de Rendimento Escolar (INEP) ===")
    base_dir = Path(__file__).resolve().parent.parent.parent
    raw_dir = base_dir / "data" / "raw" / "rendimento"

    zips = sorted(raw_dir.glob("tx_rend_escolas_*.zip"))
    if not zips:
        raise FileNotFoundError(f"Nenhum arquivo zip encontrado em {raw_dir}")

    print(f"Arquivos zip localizados ({len(zips)}): {[z.name for z in zips]}")

    dfs_pr = []

    for zpath in zips:
        ano_str = zpath.stem.split("_")[-1]
        print(f"\nProcessando ano {ano_str} ({zpath.name})...")

        with zipfile.ZipFile(zpath) as z:
            xlsx_names = [n for n in z.namelist() if n.endswith(".xlsx")]
            if not xlsx_names:
                print(f"  AVISO: Nenhum arquivo .xlsx encontrado no zip {zpath.name}")
                continue

            excel_name = xlsx_names[0]
            print(f"  Lendo planilha: {excel_name} com engine calamine...")
            with z.open(excel_name) as f:
                df_head = pd.read_excel(f, skiprows=7, nrows=2, engine="calamine")
                cols = df_head.columns.tolist()

            with z.open(excel_name) as f:
                df = pd.read_excel(f, skiprows=8, engine="calamine")

            # Coluna 2 é SG_UF
            uf_col = df.columns[2]
            df_pr = df[df[uf_col] == "PR"].copy()
            print(f"  Total de escolas do Paraná encontradas: {len(df_pr)}")

            # Mapear colunas posicionais estáveis
            # 0: Ano, 2: SG_UF, 3: CO_MUNICIPIO, 4: NO_MUNICIPIO, 5: CO_ENTIDADE, 6: NO_ENTIDADE, 8: NO_DEPENDENCIA
            # 10: Aprov AI, 11: Aprov AF, 21: Aprov MED
            # 28: Reprov AI, 29: Reprov AF, 39: Reprov MED
            # 46: Aband AI, 47: Aband AF, 57: Aband MED
            sub_pr = pd.DataFrame({
                "ANO": int(ano_str),
                "SG_UF": "PR",
                "CO_MUNICIPIO": df_pr.iloc[:, 3].astype(str).str.replace(r"\.0$", "", regex=True),
                "NO_MUNICIPIO": df_pr.iloc[:, 4].astype(str),
                "CO_ENTIDADE": pd.to_numeric(df_pr.iloc[:, 5], errors="coerce").astype("Int64"),
                "NO_ENTIDADE": df_pr.iloc[:, 6].astype(str),
                "NO_DEPENDENCIA": df_pr.iloc[:, 8].astype(str),

                # Aprovação
                "APROV_ANOS_INICIAIS": df_pr.iloc[:, 10].astype(str),
                "APROV_ANOS_FINAIS": df_pr.iloc[:, 11].astype(str),
                "APROV_ENSINO_MEDIO": df_pr.iloc[:, 21].astype(str),

                # Reprovação
                "REPROV_ANOS_INICIAIS": df_pr.iloc[:, 28].astype(str),
                "REPROV_ANOS_FINAIS": df_pr.iloc[:, 29].astype(str),
                "REPROV_ENSINO_MEDIO": df_pr.iloc[:, 39].astype(str),

                # Abandono
                "ABAND_ANOS_INICIAIS": df_pr.iloc[:, 46].astype(str),
                "ABAND_ANOS_FINAIS": df_pr.iloc[:, 47].astype(str),
                "ABAND_ENSINO_MEDIO": df_pr.iloc[:, 57].astype(str),
            })

            dfs_pr.append(sub_pr)

    df_consolidado = pd.concat(dfs_pr, ignore_index=True)
    df_consolidado = df_consolidado[df_consolidado["CO_ENTIDADE"].notna()].copy()
    df_consolidado["CO_ENTIDADE"] = df_consolidado["CO_ENTIDADE"].astype(int)

    out_raw = raw_dir / "rendimento_parana_raw.parquet"
    df_consolidado.to_parquet(out_raw, index=False)

    print(f"\n=== Importação Concluída com Sucesso! ===")
    print(f"Arquivo gerado: {out_raw} ({len(df_consolidado)} registros de escolas x anos)")
    print(df_consolidado.groupby("ANO")["CO_ENTIDADE"].count().to_string())

if __name__ == "__main__":
    run()
