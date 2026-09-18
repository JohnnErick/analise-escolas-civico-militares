import unittest
import pandas as pd
import numpy as np

from modules.data_loader import (
    load_cadastro,
    load_saeb_tidy,
    load_rendimento_tidy,
    load_ideb_tidy,
    get_school_ccm_status
)
from modules.views_school_detail import calculate_before_after_metrics

class TestSchoolDetailBeforeAfter(unittest.TestCase):

    def setUp(self):
        self.df_cad = load_cadastro()
        self.df_saeb = load_saeb_tidy()
        self.df_rend = load_rendimento_tidy()
        self.df_ideb = load_ideb_tidy()

    def test_get_school_ccm_status_coorte_2021(self):
        # Colégio Estadual Cívico-Militar Prefeito Carlos Massaretto
        inep_2021 = 41025482
        sub = self.df_cad[self.df_cad["codigo_inep"] == inep_2021]
        self.assertFalse(sub.empty)
        row = sub.iloc[0]

        is_cm, ano, label = get_school_ccm_status(inep_2021, row)
        self.assertTrue(is_cm)
        self.assertEqual(ano, 2021)
        self.assertIn("2021", label)

    def test_get_school_ccm_status_coorte_2024(self):
        # Colégio Estadual Professor Alberto Krause
        inep_2024 = 41122801
        sub = self.df_cad[self.df_cad["codigo_inep"] == inep_2024]
        self.assertFalse(sub.empty)
        row = sub.iloc[0]

        is_cm, ano, label = get_school_ccm_status(inep_2024, row)
        self.assertTrue(is_cm)
        self.assertEqual(ano, 2024)
        self.assertIn("2024", label)

    def test_get_school_ccm_status_regular(self):
        # Escola regular não cívico-militar
        inep_regular = 41000129
        sub = self.df_cad[self.df_cad["codigo_inep"] == inep_regular]
        self.assertFalse(sub.empty)
        row = sub.iloc[0]

        is_cm, ano, label = get_school_ccm_status(inep_regular, row)
        self.assertFalse(is_cm)
        self.assertIsNone(ano)

    def test_calculate_before_after_metrics_sample(self):
        inep = 41025482
        etapa = "Anos Finais (6º-9º)"
        ano_transicao = 2021

        sub_saeb = self.df_saeb[(self.df_saeb["ID_ESCOLA"] == inep) & (self.df_saeb["ETAPA"] == etapa)]
        sub_rend = self.df_rend[(self.df_rend["ID_ESCOLA"] == inep) & (self.df_rend["ETAPA"] == etapa)]
        sub_ideb = self.df_ideb[(self.df_ideb["ID_ESCOLA"] == inep) & (self.df_ideb["ETAPA"] == etapa)]

        df_metrics = calculate_before_after_metrics(sub_saeb, sub_rend, sub_ideb, ano_transicao)
        self.assertFalse(df_metrics.empty)
        self.assertIn("id", df_metrics.columns)
        self.assertIn("media_antes", df_metrics.columns)
        self.assertIn("media_depois", df_metrics.columns)
        self.assertIn("delta", df_metrics.columns)

        # Checar métricas do IDEB
        ideb_row = df_metrics[df_metrics["id"] == "IDEB_OBSERVADO"].iloc[0]
        self.assertAlmostEqual(ideb_row["media_antes"], 3.925, places=2)
        self.assertAlmostEqual(ideb_row["media_depois"], 4.900, places=2)
        self.assertAlmostEqual(ideb_row["delta"], 0.975, places=2)
        self.assertEqual(ideb_row["n_antes"], 8)
        self.assertEqual(ideb_row["n_depois"], 2)

        # Checar taxa de aprovação
        aprov_row = df_metrics[df_metrics["id"] == "TAXA_APROVACAO"].iloc[0]
        self.assertAlmostEqual(aprov_row["media_antes"], 83.725, places=2)
        self.assertAlmostEqual(aprov_row["media_depois"], 88.500, places=2)
        self.assertAlmostEqual(aprov_row["delta"], 4.775, places=2)

if __name__ == "__main__":
    unittest.main()
