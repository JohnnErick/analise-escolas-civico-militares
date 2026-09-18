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
from modules.views_evolution import build_baseline_dataset

class TestViewsDataIntegration(unittest.TestCase):

    def test_overview_aggregations(self):
        df_cad = load_cadastro()
        df_hist = load_historico_ano()
        
        total_base = len(df_cad)
        self.assertEqual(total_base, 5966)
        
        ccm_2024 = len(df_cad[df_cad["ano_inicio_ccm"] == "2024"])
        ccm_2026 = len(df_cad[df_cad["ano_inicio_ccm"] == "2026"])
        ccm_ind = len(df_cad[df_cad["ano_inicio_ccm"] == "INDETERMINADO"])
        
        self.assertEqual(ccm_2024, 106)
        self.assertEqual(ccm_2026, 33)
        self.assertEqual(ccm_ind, 62)
        self.assertEqual(ccm_2024 + ccm_2026 + ccm_ind, 201)
        
        tab_status_ano = df_hist.groupby(["ano", "civico_militar"]).size().unstack(fill_value=0)
        self.assertEqual(tab_status_ano.loc[2024, "SIM"], 106)
        self.assertEqual(tab_status_ano.loc[2026, "SIM"], 139)
        self.assertEqual(tab_status_ano.loc[2020, "INDETERMINADO"], 201)

    def test_baseline_dataset_groups(self):
        data = build_baseline_dataset()
        cad = data["cad"]
        self.assertIn("GRUPO_ANALITICO", cad.columns)
        
        counts = cad["GRUPO_ANALITICO"].value_counts()
        self.assertEqual(counts["CCM 2024"], 106)
        self.assertEqual(counts["Consultadas não convertidas"], 62)
        self.assertEqual(counts["Rede regular"], 1816)

    def test_school_detail_data_fetch(self):
        df_cad = load_cadastro()
        df_hist = load_historico_ano()
        df_ev = load_historico_eventos()
        df_saeb = load_saeb_tidy()
        df_rend = load_rendimento_tidy()
        df_ideb = load_ideb_tidy()
        
        inep = 41000021
        esc = df_cad[df_cad["codigo_inep"] == inep]
        self.assertFalse(esc.empty)
        
        hist = df_hist[df_hist["codigo_inep"] == inep]
        self.assertEqual(len(hist), 7)
        
        ev = df_ev[df_ev["codigo_inep_num"] == inep]
        self.assertGreater(len(ev), 0)
        
        saeb = df_saeb[df_saeb["ID_ESCOLA"] == inep]
        self.assertFalse(saeb.empty)
        
        rend = df_rend[df_rend["ID_ESCOLA"] == inep]
        self.assertFalse(rend.empty)
        
        ideb = df_ideb[df_ideb["ID_ESCOLA"] == inep]
        self.assertFalse(ideb.empty)

if __name__ == "__main__":
    unittest.main()
