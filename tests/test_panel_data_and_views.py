import unittest
import pandas as pd
import numpy as np

from modules.data_loader import (
    load_cadastro,
    load_historico_ano,
    load_historico_eventos,
    load_saeb_tidy,
    load_rendimento_tidy,
    load_ideb_tidy
)

class TestPanelDataAndQuality(unittest.TestCase):

    def test_load_cadastro(self):
        df_cad = load_cadastro()
        self.assertFalse(df_cad.empty)
        self.assertEqual(len(df_cad), 5966)
        self.assertIn("codigo_inep", df_cad.columns)
        self.assertIn("nome_escola", df_cad.columns)
        self.assertIn("municipio", df_cad.columns)
        self.assertIn("latitude", df_cad.columns)
        self.assertIn("longitude", df_cad.columns)
        self.assertIn("tipo_coordenada", df_cad.columns)
        
        # Validações de integridade
        self.assertEqual(df_cad["latitude"].notna().sum(), 5966)
        self.assertEqual(df_cad["longitude"].notna().sum(), 5966)
        self.assertTrue(set(df_cad["tipo_coordenada"].unique()).issubset({"EXATA_KML", "CENTROIDE_MUNICIPIO"}))
        
        # 201 escolas CCM auditadas
        self.assertEqual(df_cad["is_ccm"].sum(), 201)

    def test_load_historico_ano(self):
        df_hist = load_historico_ano()
        self.assertFalse(df_hist.empty)
        self.assertEqual(len(df_hist), 1407)  # 201 escolas x 7 anos
        self.assertEqual(df_hist["codigo_inep"].nunique(), 201)
        self.assertEqual(sorted(df_hist["ano"].unique().tolist()), [2020, 2021, 2022, 2023, 2024, 2025, 2026])
        
        # Status permitidos
        status_unicos = set(df_hist["civico_militar"].unique())
        self.assertTrue(status_unicos.issubset({"SIM", "NAO", "INDETERMINADO"}))
        
        # Contagens auditadas
        counts = df_hist["civico_militar"].value_counts()
        self.assertEqual(counts["INDETERMINADO"], 846)
        self.assertEqual(counts["SIM"], 351)
        self.assertEqual(counts["NAO"], 210)

    def test_load_historico_eventos(self):
        df_ev = load_historico_eventos()
        self.assertFalse(df_ev.empty)
        self.assertEqual(len(df_ev), 384)
        self.assertIn("tipo_evento", df_ev.columns)
        self.assertIn("documento_origem", df_ev.columns)
        self.assertIn("pagina_origem", df_ev.columns)
        self.assertIn("data_documento", df_ev.columns)

    def test_load_saeb_tidy_quality(self):
        df_saeb = load_saeb_tidy()
        self.assertFalse(df_saeb.empty)
        self.assertIn("ID_ESCOLA", df_saeb.columns)
        self.assertIn("SAEB_PORTUGUES", df_saeb.columns)
        self.assertIn("SAEB_MATEMATICA", df_saeb.columns)
        self.assertIn("STATUS_PARTICIPACAO_SAEB", df_saeb.columns)
        
        # Regra crucial: ausência de notas NÃO deve ser preenchida com zero
        nd_rows = df_saeb[df_saeb["STATUS_PARTICIPACAO_SAEB"] == "NAO_DIVULGADO_MENOS_10_ALUNOS_OU_BAIXA_PARTICIPACAO"]
        if not nd_rows.empty:
            self.assertTrue(nd_rows["SAEB_PORTUGUES"].isna().all())
            self.assertTrue(nd_rows["SAEB_MATEMATICA"].isna().all())

    def test_load_rendimento_tidy_quality(self):
        df_rend = load_rendimento_tidy()
        self.assertFalse(df_rend.empty)
        self.assertIn("TAXA_APROVACAO", df_rend.columns)
        self.assertIn("TAXA_REPROVACAO", df_rend.columns)
        self.assertIn("TAXA_ABANDONO", df_rend.columns)
        
        # Anos esperados presentes
        self.assertIn(2023, df_rend["ANO"].values)
        self.assertIn(2017, df_rend["ANO"].values)

    def test_load_ideb_tidy_quality(self):
        df_ideb = load_ideb_tidy()
        self.assertFalse(df_ideb.empty)
        self.assertIn("IDEB_OBSERVADO", df_ideb.columns)
        self.assertIn("IDEB_META", df_ideb.columns)
        self.assertIn("ANO_IDEB", df_ideb.columns)

    def test_schools_foreign_keys(self):
        df_cad = load_cadastro()
        df_hist = load_historico_ano()
        df_ev = load_historico_eventos()
        
        ineps_cad = set(df_cad["codigo_inep"])
        ineps_hist = set(df_hist["codigo_inep"])
        self.assertTrue(ineps_hist.issubset(ineps_cad))
        
        ineps_ev = set(df_ev["codigo_inep_num"].dropna().astype(int))
        self.assertTrue(ineps_ev.issubset(ineps_cad))

if __name__ == "__main__":
    unittest.main()
