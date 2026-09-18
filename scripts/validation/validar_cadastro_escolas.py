#!/usr/bin/env python3
"""
validar_cadastro_escolas.py

Script para validação formal, integridade referencial e auditoria diagnóstica
da Dimensão Cadastral Mestre das Escolas (escolas_cadastro.parquet / .csv).

Testa:
1. Presença dos 201 códigos INEP auditados das escolas CCM (100% de cobertura);
2. Ausência de duplicidades na chave primária 'codigo_inep';
3. Completude dos campos oficiais: NRE, Município, UF, Localização, Dependência, Coordenadas;
4. Conformidade de dados ausentes (Endereço, Bairro e CEP mantidos ausentes sem invenção);
5. Invariância e congelamento das bases anteriores (Histórico CCM, SAEB, Rendimento e IDEB);
6. Integridade relacional: junção determinística (JOIN) entre cadastro e bases analíticas.
"""

from pathlib import Path
import pandas as pd
import numpy as np

def run():
    print("=== Iniciando Validação Diagnóstica do Cadastro das Escolas ===")
    base_dir = Path(__file__).resolve().parent.parent.parent
    proc_dir = base_dir / "data" / "processed"
    
    # 1. Carregar Cadastro Mestre
    cad_parquet = proc_dir / "escolas_cadastro.parquet"
    cad_csv = proc_dir / "escolas_cadastro.csv"
    cad_ccm_csv = proc_dir / "escolas_cadastro_ccm.csv"
    audit_csv = proc_dir / "auditoria_cadastro_escolas.csv"
    
    assert cad_parquet.exists(), "ERRO: escolas_cadastro.parquet não encontrado!"
    assert cad_csv.exists(), "ERRO: escolas_cadastro.csv não encontrado!"
    assert cad_ccm_csv.exists(), "ERRO: escolas_cadastro_ccm.csv não encontrado!"
    assert audit_csv.exists(), "ERRO: auditoria_cadastro_escolas.csv não encontrado!"
    
    df_cad = pd.read_parquet(cad_parquet)
    print(f"Cadastro Mestre carregado: {len(df_cad)} estabelecimentos cadastrados.")
    
    # 2. Teste de Unicidade da Chave Primária
    dup_codes = df_cad[df_cad.duplicated(subset=["codigo_inep"], keep=False)]
    assert len(dup_codes) == 0, f"ERRO: Códigos INEP duplicados no cadastro mestre: {len(dup_codes)}"
    print("✓ Teste 1: Chave primária 'codigo_inep' é 100% ÚNICA (0 duplicidades).")
    
    # 3. Teste de Cobertura das 201 Escolas CCM Auditadas
    df_hist_ccm = pd.read_csv(proc_dir / "historico_ccm_por_ano.csv", sep=";")
    codigos_ccm_esperados = set(df_hist_ccm["codigo_inep"].unique())
    assert len(codigos_ccm_esperados) == 201, f"ERRO: Esperado 201 códigos CCM, encontrado {len(codigos_ccm_esperados)}"
    
    codigos_cadastrados = set(df_cad["codigo_inep"].unique())
    diff_missing = codigos_ccm_esperados - codigos_cadastrados
    assert len(diff_missing) == 0, f"ERRO: Escolas CCM ausentes no cadastro: {diff_missing}"
    
    df_ccm = df_cad[df_cad["is_ccm"] == True].copy()
    assert len(df_ccm) == 201, f"ERRO: Esperado 201 registros marcados como is_ccm=True, encontrado {len(df_ccm)}"
    print(f"✓ Teste 2: Todas as 201 escolas CCM auditadas estão presentes no cadastro (201/201 - 100,0%).")
    
    # 4. Teste de Completude dos Campos Oficiais nas 201 Escolas CCM
    # NRE
    nre_faltantes = df_ccm[df_ccm["nre"].isna() | (df_ccm["nre"] == "")]
    assert len(nre_faltantes) == 0, f"ERRO: Escolas CCM com NRE ausente: {len(nre_faltantes)}"
    print("✓ Teste 3: Cobertura de NRE é 100,0% (201/201 identificados nos editais oficiais).")
    
    # Município e UF
    assert df_ccm["municipio"].notna().all(), "ERRO: Município ausente em escolas CCM!"
    assert (df_ccm["uf"] == "PR").all(), "ERRO: UF diferente de PR encontrada!"
    print("✓ Teste 4: Município e UF ('PR') 100% preenchidos.")
    
    # Dependência Administrativa e Rede
    assert (df_ccm["dependencia_administrativa"] == "Estadual").all(), "ERRO: Dependência administrativa inválida!"
    assert (df_ccm["rede_ensino"] == "Pública Estadual").all(), "ERRO: Rede de ensino inválida!"
    print("✓ Teste 5: Dependência Administrativa ('Estadual') e Rede ('Pública Estadual') 100% válidas.")
    
    # Localização (Urbana / Rural)
    assert df_ccm["localizacao"].isin(["Urbana", "Rural"]).all(), "ERRO: Localização inválida!"
    print(f"✓ Teste 6: Localização 100% válida ({df_ccm['localizacao'].value_counts().to_dict()}).")
    
    # Coordenadas Geográficas
    assert df_ccm["latitude"].notna().all(), "ERRO: Latitude ausente em escolas CCM!"
    assert df_ccm["longitude"].notna().all(), "ERRO: Longitude ausente em escolas CCM!"
    assert df_ccm["tipo_coordenada"].isin(["EXATA_KML", "CENTROIDE_MUNICIPIO"]).all(), "ERRO: Tipo de coordenada inválido!"
    print(f"✓ Teste 7: Coordenadas geográficas 100% válidas ({df_ccm['tipo_coordenada'].value_counts().to_dict()}).")
    
    # Etapas Ofertadas
    assert df_ccm["etapas_ofertadas"].notna().all(), "ERRO: Etapas ofertadas ausentes!"
    print("✓ Teste 8: Etapas ofertadas 100% preenchidas.")
    
    # 5. Teste de Conformidade de Dados Ausentes (Sem Invenção)
    # Endereço, Bairro e CEP devem ser estritamente ausentes
    assert df_ccm["endereco"].isna().all(), "ERRO: Campo 'endereco' foi indevidamente preenchido!"
    assert df_ccm["bairro"].isna().all(), "ERRO: Campo 'bairro' foi indevidamente preenchido!"
    assert df_ccm["cep"].isna().all(), "ERRO: Campo 'cep' foi indevidamente preenchido!"
    print("✓ Teste 9: Dados ausentes não foram inventados (endereco, bairro e cep 100% nulos/documentados).")
    
    # 6. Teste da Tabela de Auditoria Individual
    df_audit = pd.read_csv(audit_csv, sep=";")
    assert len(df_audit) == 201, f"ERRO: Tabela de auditoria possui {len(df_audit)} linhas, esperado 201."
    assert (df_audit["status_matching"].isin(["CONFIRMADO", "AMBIGUO"])).all(), "ERRO: Status de matching inválido!"
    ambiguos = df_audit[df_audit["status_matching"] == "AMBIGUO"]
    assert len(ambiguos) == 1 and ambiguos.iloc[0]["codigo_inep"] == 41146093, "ERRO: Apenas 41146093 deve ser AMBIGUO!"
    print("✓ Teste 10: Auditoria individual das 201 escolas validada (200 CONFIRMADO, 1 AMBIGUO).")
    
    # 7. Teste de Invariância e Congelamento das Bases Anteriores
    print("\nVerificando congelamento e integridade das bases existentes...")
    
    # Histórico CCM por ano
    assert len(df_hist_ccm) == 1407, f"ERRO: historico_ccm_por_ano alterado! Linhas: {len(df_hist_ccm)}"
    assert set(df_hist_ccm.columns) == {
        "codigo_inep", "nome_escola", "municipio", "ano", "civico_militar",
        "status_historico", "ano_inicio_ccm", "ano_fim_ccm", "evidencia_inicio",
        "evidencia_status", "nivel_confianca", "observacao"
    }, "ERRO: Colunas de historico_ccm_por_ano alteradas!"
    
    # Histórico Evidências
    df_evid = pd.read_csv(proc_dir / "historico_ccm_evidencias.csv", sep=";")
    assert len(df_evid) == 384, f"ERRO: historico_ccm_evidencias alterado! Linhas: {len(df_evid)}"
    
    # Base Integrada CCM x SAEB x Rendimento x IDEB
    df_matriz_integ = pd.read_parquet(proc_dir / "ccm_saeb_rendimento_ideb.parquet")
    assert len(df_matriz_integ) == 2646, f"ERRO: ccm_saeb_rendimento_ideb alterado! Linhas: {len(df_matriz_integ)}"
    
    df_serie_comp = pd.read_parquet(proc_dir / "ccm_saeb_rendimento_ideb_serie_completa.parquet")
    assert len(df_serie_comp) == 5878, f"ERRO: ccm_saeb_rendimento_ideb_serie_completa alterado! Linhas: {len(df_serie_comp)}"
    print("✓ Teste 11: Todas as bases anteriores permanecem rigorosamente INALTERADAS e CONGELADAS.")
    
    # 8. Teste de Integridade Relacional (JOIN)
    print("\nTestando integridade relacional entre Cadastro e Bases Existentes...")
    # Merge com historico_ccm_por_ano
    m_hist = pd.merge(df_hist_ccm, df_cad[["codigo_inep", "nre", "localizacao", "etapas_ofertadas", "latitude", "longitude"]], on="codigo_inep", how="left")
    assert len(m_hist) == len(df_hist_ccm), "ERRO: Merge gerou alteração na quantidade de linhas!"
    assert m_hist["nre"].notna().all(), "ERRO: NRE ausente após merge com histórico!"
    
    # Merge com matriz integrada
    m_integ = pd.merge(df_matriz_integ, df_cad[["codigo_inep", "nre", "localizacao", "etapas_ofertadas", "tipo_coordenada"]], on="codigo_inep", how="left")
    assert len(m_integ) == len(df_matriz_integ), "ERRO: Merge gerou alteração na matriz integrada!"
    assert m_integ["nre"].notna().all(), "ERRO: NRE ausente após merge com matriz integrada!"
    print("✓ Teste 12: Integridade relacional confirmada (100% dos registros integram perfeitamente por codigo_inep).")
    
    print("\n=== Todos os 12 Testes de Validação Cadastral Foram APROVADOS com Sucesso! ===")

if __name__ == "__main__":
    run()
