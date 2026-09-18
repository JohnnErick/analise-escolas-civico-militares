import unittest
import pandas as pd
import numpy as np
from modules.data_loader import load_comparisons_dataset

class TestOverviewComparison(unittest.TestCase):

    def setUp(self):
        self.df = load_comparisons_dataset()

    def test_dataset_loaded_properly(self):
        self.assertFalse(self.df.empty)
        required_cols = ["ID_ESCOLA", "ANO", "ETAPA", "REDE", "TIPO_GESTAO", "TAXA_APROVACAO", "SAEB_PORTUGUES", "SAEB_MATEMATICA", "IDEB_OBSERVADO"]
        for col in required_cols:
            self.assertIn(col, self.df.columns)

    def test_metrics_calculation_2023_anos_finais(self):
        sub = self.df[(self.df["ANO"] == 2023) & (self.df["REDE"] == "Estadual") & (self.df["ETAPA"] == "Anos Finais (6º-9º)")]
        self.assertFalse(sub.empty)

        ccm_sub = sub[sub["TIPO_GESTAO"] == "Cívico-Militar"]
        reg_sub = sub[sub["TIPO_GESTAO"] == "Não Cívico-Militar"]

        self.assertGreater(len(ccm_sub), 50)
        self.assertGreater(len(reg_sub), 500)

        # Aprovação
        ccm_aprov = ccm_sub["TAXA_APROVACAO"].dropna().mean()
        reg_aprov = reg_sub["TAXA_APROVACAO"].dropna().mean()
        self.assertGreater(ccm_aprov, 90.0)
        self.assertGreater(reg_aprov, 90.0)

        # SAEB Língua Portuguesa
        ccm_lp = ccm_sub["SAEB_PORTUGUES"].dropna().mean()
        reg_lp = reg_sub["SAEB_PORTUGUES"].dropna().mean()
        self.assertGreater(ccm_lp, 200.0)
        self.assertGreater(reg_lp, 200.0)

        # SAEB Matemática
        ccm_mt = ccm_sub["SAEB_MATEMATICA"].dropna().mean()
        reg_mt = reg_sub["SAEB_MATEMATICA"].dropna().mean()
        self.assertGreater(ccm_mt, 200.0)
        self.assertGreater(reg_mt, 200.0)

        # IDEB
        ccm_ideb = ccm_sub["IDEB_OBSERVADO"].dropna().mean()
        reg_ideb = reg_sub["IDEB_OBSERVADO"].dropna().mean()
        self.assertGreater(ccm_ideb, 4.0)
        self.assertGreater(reg_ideb, 4.0)

    def test_metrics_calculation_2023_ensino_medio(self):
        sub = self.df[(self.df["ANO"] == 2023) & (self.df["REDE"] == "Estadual") & (self.df["ETAPA"] == "Ensino Médio")]
        self.assertFalse(sub.empty)

        ccm_sub = sub[sub["TIPO_GESTAO"] == "Cívico-Militar"]
        reg_sub = sub[sub["TIPO_GESTAO"] == "Não Cívico-Militar"]

        self.assertGreater(len(ccm_sub), 50)
        self.assertGreater(len(reg_sub), 500)

        ccm_ideb = ccm_sub["IDEB_OBSERVADO"].dropna().mean()
        reg_ideb = reg_sub["IDEB_OBSERVADO"].dropna().mean()
        self.assertGreater(ccm_ideb, 3.5)
        self.assertGreater(reg_ideb, 3.5)

if __name__ == "__main__":
    unittest.main()
