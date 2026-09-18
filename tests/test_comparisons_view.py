import unittest
import pandas as pd
import numpy as np

from modules.data_loader import load_comparisons_dataset

class TestComparisonsViewData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.df = load_comparisons_dataset()

    def test_dataset_not_empty_and_required_columns(self):
        self.assertFalse(self.df.empty)
        self.assertGreater(len(self.df), 50000)

        required_columns = [
            "ID_ESCOLA", "NO_ESCOLA", "NO_MUNICIPIO", "REDE", "ETAPA", "ANO",
            "TIPO_GESTAO", "TAXA_APROVACAO", "TAXA_NAO_APROVACAO",
            "TAXA_REPROVACAO", "TAXA_ABANDONO",
            "SAEB_PORTUGUES", "SAEB_MATEMATICA", "SAEB_NOTA_MEDIA",
            "IDEB_OBSERVADO", "DELTA_META_IDEB",
            "status_ccm_atual", "is_ccm"
        ]
        for col in required_columns:
            self.assertIn(col, self.df.columns, f"Coluna obrigatória '{col}' não encontrada no dataset comparativo.")

    def test_approval_rates_ranges(self):
        # Taxa de aprovação deve estar entre 0 e 100
        valid_aprov = self.df["TAXA_APROVACAO"].dropna()
        self.assertTrue((valid_aprov >= 0).all())
        self.assertTrue((valid_aprov <= 100.01).all())

        # Taxa de não-aprovação deve complementar taxa de aprovação
        valid_both = self.df.dropna(subset=["TAXA_APROVACAO", "TAXA_NAO_APROVACAO"])
        diff = (valid_both["TAXA_APROVACAO"] + valid_both["TAXA_NAO_APROVACAO"]) - 100.0
        self.assertTrue((diff.abs() < 1e-3).all())

    def test_flow_indicators_census(self):
        # Reprovação e abandono devem ter registros não nulos
        self.assertGreater(self.df["TAXA_REPROVACAO"].notna().sum(), 20000)
        self.assertGreater(self.df["TAXA_ABANDONO"].notna().sum(), 20000)

    def test_comparisons_group_aggregations_2023_anos_finais(self):
        sub = self.df[(self.df["ANO"] == 2023) & (self.df["ETAPA"] == "Anos Finais (6º-9º)")].copy()
        self.assertFalse(sub.empty)

        # Agrupamento CCM vs Estadual Regular
        cm = sub[sub["TIPO_GESTAO"] == "Cívico-Militar"]
        ncm_est = sub[(sub["TIPO_GESTAO"] == "Não Cívico-Militar") & (sub["REDE"] == "Estadual")]

        self.assertGreater(len(cm), 100)
        self.assertGreater(len(ncm_est), 1000)

        # Médias de aprovação devem ser calculáveis e estar no intervalo plausível
        mean_aprov_cm = cm["TAXA_APROVACAO"].mean()
        mean_aprov_ncm = ncm_est["TAXA_APROVACAO"].mean()

        self.assertTrue(pd.notna(mean_aprov_cm))
        self.assertTrue(pd.notna(mean_aprov_ncm))
        self.assertGreater(mean_aprov_cm, 70.0)
        self.assertGreater(mean_aprov_ncm, 70.0)

        # Médias SAEB
        mean_saeb_cm = cm["SAEB_NOTA_MEDIA"].mean()
        mean_saeb_ncm = ncm_est["SAEB_NOTA_MEDIA"].mean()
        self.assertTrue(pd.notna(mean_saeb_cm))
        self.assertTrue(pd.notna(mean_saeb_ncm))

    def test_approval_brackets_calculation(self):
        sub = self.df[(self.df["ANO"] == 2023) & (self.df["ETAPA"] == "Anos Finais (6º-9º)")].copy()
        bins = [-np.inf, 85.0, 90.0, 95.0, 98.0, 99.99, 100.01]
        labels = ["< 85%", "85% a 90%", "90% a 95%", "95% a 98%", "98% a 99.9%", "100% (Plena)"]
        sub["FAIXA"] = pd.cut(sub["TAXA_APROVACAO"], bins=bins, labels=labels, right=False)

        tab = pd.crosstab(sub["FAIXA"], sub["TIPO_GESTAO"], normalize="columns") * 100
        # A soma de cada coluna da tabela cruzada deve ser 100% (com tolerância de arredondamento)
        for col in tab.columns:
            self.assertAlmostEqual(tab[col].sum(), 100.0, places=1)

    def test_grade_level_columns_presence(self):
        for g_col in ["TAXA_APROVACAO_1", "TAXA_APROVACAO_2", "TAXA_APROVACAO_3", "TAXA_APROVACAO_4"]:
            self.assertIn(g_col, self.df.columns)
            self.assertGreater(self.df[g_col].notna().sum(), 10000)

if __name__ == "__main__":
    unittest.main()
