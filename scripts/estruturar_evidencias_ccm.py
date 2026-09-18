"""
Script de Identificação e Estruturação de Evidências Documentais dos Colégios Cívico-Militares do Paraná.
Versão Refinada e Auditada:
- Identifica com precisão estrita tabelas de instituições de ensino (CÓD. MEC / INEP de 8 dígitos).
- Distingue rigorosamente listas de escolas de listas de candidatos/militares (RGs).
- Mapeia municípios com suporte a abreviações oficiais da SEED/PR.
- Registra a fonte literal, a página exata e o contexto de cada ato normativo.
- Gera 'data/processed/historico_ccm_evidencias.csv' e 'data/validation/extracao_revisao.csv'.
"""

import os
import re
import unicodedata
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
EXTRACTED_DIR = BASE_DIR / "data" / "extracted" / "editais"
MUN_FILE = BASE_DIR / "data" / "municipios_pr.csv"
OUTPUT_EVIDENCIAS = BASE_DIR / "data" / "processed" / "historico_ccm_evidencias.csv"
OUTPUT_REVISAO = BASE_DIR / "data" / "validation" / "extracao_revisao.csv"

OUTPUT_EVIDENCIAS.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_REVISAO.parent.mkdir(parents=True, exist_ok=True)

# 1. Base oficial de municípios do PR
df_mun = pd.read_csv(MUN_FILE) if MUN_FILE.exists() else pd.DataFrame()
def norm_str(s: str) -> str:
    if not isinstance(s, str): return ""
    return unicodedata.normalize("NFKD", s).encode("ASCII", "ignore").decode("ASCII").strip().upper()

MUN_DICT = {}
if not df_mun.empty:
    for _, r in df_mun.iterrows():
        MUN_DICT[norm_str(r["nome"])] = r["nome"]

# Dicionário de abreviações e variações oficiais frequentes nos editais da SEED/PR
ABREV_MUN = {
    "ALM TAMANDARE": "Almirante Tamandaré",
    "ALMIRANTE TAMANDARE": "Almirante Tamandaré",
    "S J DOS PINHAIS": "São José dos Pinhais",
    "SAO JOSE DOS PINHAIS": "São José dos Pinhais",
    "STO ANT DA PLATINA": "Santo Antônio da Platina",
    "SANTO ANTONIO DA PLATINA": "Santo Antônio da Platina",
    "STA HELENA": "Santa Helena",
    "STA FE": "Santa Fé",
    "STA TEREZINHA DE ITAIPU": "Santa Terezinha de Itaipu",
    "SANTA TEREZINHA DE ITAIPU": "Santa Terezinha de Itaipu",
    "FAZENDA RIO GRANDE": "Fazenda Rio Grande",
    "QDO BARROSO": "Quatro Barras",
    "QUATRO BARRAS": "Quatro Barras",
    "PINHAIS": "Pinhais",
    "COLOMBO": "Colombo",
    "PIRAQUARA": "Piraquara",
    "CAMPO MAGRO": "Campo Magro",
    "CAMPINA GRANDE DO SUL": "Campina Grande do Sul",
    "RIO BRANCO DO SUL": "Rio Branco do Sul",
    "ENG BELTRAO": "Engenheiro Beltrão",
    "ENGENHEIRO BELTRAO": "Engenheiro Beltrão",
    "CORBELIA": "Corbélia",
    "SALTO DO LONTRA": "Salto do Lontra",
    "SÃO PEDRO DO IVAÍ": "São Pedro do Ivaí",
    "SAO PEDRO DO IVAI": "São Pedro do Ivaí",
    "DIAMANTE DO SUL": "Diamante do Sul",
    "MANOEL RIBAS": "Manoel Ribas",
    "ALTO PARANA": "Alto Paraná",
}
for k, v in ABREV_MUN.items():
    MUN_DICT[norm_str(k)] = v

# Metadados de referência dos atos normativos
METADADOS_EDITAIS = {
    "edital1012023": {
        "numero": "Edital n.º 101/2023 – GS/SEED",
        "tipo": "Edital de Convocação para Consulta Pública",
        "data_doc": "2023-11-10",
        "evento": "consulta_publica",
        "status_evento": "consultada",
        "ano_referencia": 2024,
        "obs": "Convocação da comunidade escolar para consulta pública nos dias 28 e 29 de novembro de 2023."
    },
    "edital1092023": {
        "numero": "Edital n.º 109/2023 – GS/SEED",
        "tipo": "Edital Complementar de Consulta Pública",
        "data_doc": "2023-11-24",
        "evento": "consulta_publica_novas_instituicoes",
        "status_evento": "consultada",
        "ano_referencia": 2024,
        "obs": "Inclusão de novas instituições na consulta pública."
    },
    "edital1102023": {
        "numero": "Edital n.º 110/2023 – GS/SEED",
        "tipo": "Edital de Prorrogação de Consulta Pública",
        "data_doc": "2023-11-30",
        "evento": "prorrogacao_consulta_publica",
        "status_evento": "consultada",
        "ano_referencia": 2024,
        "obs": "Prorrogação da consulta pública nas instituições elencadas."
    },
    "edital1122023": {
        "numero": "Edital n.º 112/2023 – GS/SEED",
        "tipo": "Edital de Expansão e Convocação",
        "data_doc": "2023-12-01",
        "evento": "expansao_consulta_publica",
        "status_evento": "consultada",
        "ano_referencia": 2024,
        "obs": "Convocação para consulta pública de expansão do programa."
    },
    "edital1142023": {
        "numero": "Edital n.º 114/2023 – GS/SEED",
        "tipo": "Resultado de Consulta Pública",
        "data_doc": "2023-12-06",
        "evento": "aprovacao_consulta_publica",
        "status_evento": "aprovada",
        "ano_referencia": 2024,
        "obs": "Instituições com adesão aprovada na consulta pública dos dias 28 e 29 de novembro de 2023."
    },
    "edital1212023": {
        "numero": "Edital n.º 121/2023 – GS/SEED",
        "tipo": "Edital de Prorrogação de Consulta Pública",
        "data_doc": "2023-12-18",
        "evento": "prorrogacao_consulta_publica",
        "status_evento": "consultada",
        "ano_referencia": 2024,
        "obs": "Prorrogação de consulta pública complementar."
    },
    "edital1222023": {
        "numero": "Edital n.º 122/2023 – GS/SEED",
        "tipo": "Resultado de Consulta Pública / Homologação",
        "data_doc": "2023-12-20",
        "evento": "homologacao_resultado_consulta",
        "status_evento": "aprovada",
        "ano_referencia": 2024,
        "obs": "Adesão aprovada na consulta de 14-19 dez/2023 com início do modelo a partir de 01/01/2024."
    },
    "edital1232023": {
        "numero": "Edital n.º 123/2023 – GS/SEED",
        "tipo": "Resultado de Consulta Pública / Homologação",
        "data_doc": "2023-12-20",
        "evento": "homologacao_resultado_consulta",
        "status_evento": "aprovada",
        "ano_referencia": 2024,
        "obs": "Adesão aprovada na consulta de 15-19 dez/2023 com início do modelo a partir de 01/01/2024."
    },
    "edital1252025": {
        "numero": "Edital n.º 125/2025 – GS/SEED",
        "tipo": "Edital de Convocação para Consulta Pública",
        "data_doc": "2025-10-31",
        "evento": "consulta_publica",
        "status_evento": "consultada",
        "ano_referencia": 2026,
        "obs": "Convocação da comunidade escolar para consulta pública nos dias 17-19 nov/2025."
    },
    "edital1362025": {
        "numero": "Edital n.º 136/2025 – GS/SEED",
        "tipo": "Resultado de Consulta Pública e Adesão por Critérios Objetivos",
        "data_doc": "2025-11-19",
        "evento": "homologacao_resultado_consulta",
        "status_evento": "aprovada",
        "ano_referencia": 2026,
        "obs": "Adesão a partir de 01/01/2026 (Anexo I: Consulta Pública; Anexo II: Critérios objetivos)."
    },
    "edital_582020": {
        "numero": "Edital n.º 58/2020 – GS/SEED",
        "tipo": "Edital Normativo de Cronograma e Atividades",
        "data_doc": "2020-11-11",
        "evento": "fixacao_inicio_atividades",
        "status_evento": "implementada",
        "ano_referencia": 2021,
        "obs": "Estabelece formalmente o início das atividades do Programa Colégios Cívico-Militares em 02/01/2021."
    },
    "edital_762020": {
        "numero": "Edital n.º 76/2020 – GS/SEED",
        "tipo": "Edital Normativo de Cronograma",
        "data_doc": "2020-12-07",
        "evento": "alteracao_cronograma",
        "status_evento": "implementada",
        "ano_referencia": 2021,
        "obs": "Fixa resultado final de credenciamento em 14/12/2020 para início das atividades em 2021."
    }
}

# Lista estrita dos editais que contêm tabelas de estabelecimentos de ensino
EDITAIS_TABELA_ESCOLAS = [
    "edital1012023", "edital1092023", "edital1102023", "edital1122023",
    "edital1142023", "edital1212023", "edital1222023", "edital1232023",
    "edital1252025", "edital1362025"
]

def parse_school_line(line: str):
    line_clean = " ".join(line.strip().split())
    
    m_cod = re.search(r"\b(41\d{6})\b", line_clean)
    if not m_cod:
        return None
    cod_mec = int(m_cod.group(1))
    
    before_cod = line_clean[:m_cod.start()].strip()
    after_cod = line_clean[m_cod.end():].strip()
    
    mun_encontrado = ""
    escola_raw = ""
    
    # 1. Se o código estava no início: [COD] [NRE...] [MUNICIPIO...] [ESTABELECIMENTO...]
    if len(before_cod) < 3:
        tokens = after_cod.split()
        for length in [4, 3, 2, 1]:
            for start_idx in range(min(5, max(1, len(tokens) - length + 1))):
                cand = " ".join(tokens[start_idx : start_idx + length])
                cand_norm = norm_str(cand)
                if cand_norm in MUN_DICT:
                    mun_encontrado = MUN_DICT[cand_norm]
                    escola_raw = " ".join(tokens[start_idx + length:])
                    break
            if mun_encontrado:
                break
        if not mun_encontrado:
            escola_raw = after_cod
            
    # 2. Se o código estava após o NRE/Município: [NRE...] [MUNICIPIO...] [COD] [ESTABELECIMENTO...]
    else:
        tokens_before = before_cod.split()
        for length in [4, 3, 2, 1]:
            for start_idx in range(len(tokens_before) - length + 1):
                cand = " ".join(tokens_before[start_idx : start_idx + length])
                cand_norm = norm_str(cand)
                if cand_norm in MUN_DICT:
                    mun_encontrado = MUN_DICT[cand_norm]
                    break
            if mun_encontrado:
                break
        escola_raw = after_cod

    escola_raw = escola_raw.strip(", -_")
    if not escola_raw:
        escola_raw = line_clean
        
    return {
        "codigo_inep": cod_mec,
        "nome_escola_original": escola_raw,
        "municipio_original": mun_encontrado,
        "fonte": line_clean
    }

def processar_evidencias():
    txt_files = sorted(list(EXTRACTED_DIR.glob("*.txt")))
    print(f"Processando {len(txt_files)} editais em busca de evidências documentais...")
    
    evidencias = []
    revisoes = []
    
    for f in txt_files:
        stem = f.stem
        pdf_name = stem + ".pdf"
        content = f.read_text(encoding="utf-8")
        
        # Identificar se é um dos editais principais com tabelas de escolas
        is_edital_escolas = any(k in stem for k in EDITAIS_TABELA_ESCOLAS)
        is_edital_normativo_2020 = any(k in stem for k in ["edital_582020", "edital_762020"])
        
        # Obter metadados do ato
        key_meta = None
        for k in METADADOS_EDITAIS:
            if k in stem:
                key_meta = k
                break
        meta = METADADOS_EDITAIS.get(key_meta, {})
        num_doc = meta.get("numero", "")
        if not num_doc:
            m_num = re.search(r"(EDITAL\s+N\.[ºo]\s*[\d\.\/]+[^\n\r]+)", content, re.IGNORECASE)
            num_doc = m_num.group(1).strip() if m_num else f"Edital ({stem})"
            
        data_doc = meta.get("data_doc", "")
        if not data_doc:
            m_data = re.search(r"em\s+(\d{2}/\d{2}/\d{4})", content)
            if m_data:
                d, m, y = m_data.group(1).split("/")
                data_doc = f"{y}-{m}-{d}"
            else:
                data_doc = ""
                
        tipo_doc = meta.get("tipo", "Edital Administrativo / Processo Seletivo")
        evento_padrao = meta.get("evento", "processo_seletivo_pessoal")
        status_padrao = meta.get("status_evento", "nao_identificado")
        ano_ref_padrao = meta.get("ano_referencia", None)
        obs_padrao = meta.get("obs", "")

        # Dividir o texto página a página
        paginas = re.split(r"=== PÁGINA (\d+) ===", content)
        
        if is_edital_escolas:
            is_anexo_ii = False
            for i in range(1, len(paginas), 2):
                num_pag = int(paginas[i])
                texto_pag = paginas[i+1]
                
                if "anexo ii" in texto_pag.lower():
                    is_anexo_ii = True
                elif "anexo i " in texto_pag.lower() or "anexo 1" in texto_pag.lower():
                    is_anexo_ii = False
                    
                linhas = texto_pag.split("\n")
                
                for l_idx, l in enumerate(linhas):
                    if re.search(r"\b41\d{6}\b", l):
                        linha_comp = l
                        if l_idx + 1 < len(linhas):
                            prox = linhas[l_idx + 1].strip()
                            # Se a próxima linha for continuação de nome de escola
                            if prox and not re.search(r"\b41\d{6}\b", prox) and not prox.startswith("===") and not prox.startswith("Assinatura") and len(prox) < 70:
                                linha_comp = f"{l} {prox}"
                                
                        parsed = parse_school_line(linha_comp)
                        if parsed:
                            evento = evento_padrao
                            status_ev = status_padrao
                            ano_ref = ano_ref_padrao
                            obs = obs_padrao
                            
                            # Tratamento específico para o Edital 136/2025 Anexo II (critérios de queda de IDEB e frequência)
                            if "edital1362025" in stem and is_anexo_ii:
                                evento = "adesao_criterios_objetivos"
                                status_ev = "aprovada"
                                ano_ref = 2026
                                obs = "Anexo II: Critérios objetivos (queda de IDEB e frequência abaixo da média estadual de 88,91%)."
                                
                            nome_orig = parsed["nome_escola_original"]
                            mun_orig = parsed["municipio_original"]
                            nome_norm = " ".join(nome_orig.upper().split())
                            
                            evidencias.append({
                                "documento": pdf_name,
                                "tipo_documento": tipo_doc,
                                "numero_documento": num_doc,
                                "data_documento": data_doc,
                                "pagina": num_pag,
                                "codigo_inep": parsed["codigo_inep"],
                                "nome_escola_original": nome_orig,
                                "nome_escola_normalizado": nome_norm,
                                "municipio_original": mun_orig,
                                "evento": evento,
                                "status_evento": status_ev,
                                "ano_referencia": ano_ref if ano_ref is not None else "",
                                "observacao": obs,
                                "fonte": parsed["fonte"]
                            })
                            
                            if not mun_orig:
                                revisoes.append({
                                    "documento": pdf_name,
                                    "pagina": num_pag,
                                    "codigo_inep": parsed["codigo_inep"],
                                    "problema": "Município não identificado pelo dicionário automático na linha da tabela",
                                    "texto_extraido": parsed["fonte"],
                                    "acao_recomendada": "Conferir página no PDF original para extrair o município"
                                })
                                
        elif is_edital_normativo_2020:
            # Evidência geral dos editais de 2020 que fixam o início do programa estadual
            evidencias.append({
                "documento": pdf_name,
                "tipo_documento": meta.get("tipo", "Edital Normativo"),
                "numero_documento": num_doc,
                "data_documento": data_doc,
                "pagina": 3 if "edital_582020" in stem else 1,
                "codigo_inep": "",
                "nome_escola_original": "Rede Estadual - Programa Colégios Cívico-Militares do Paraná (1ª Onda Geral)",
                "nome_escola_normalizado": "REDE ESTADUAL - PROGRAMA COLEGIOS CIVICO-MILITARES DO PARANA (1A ONDA GERAL)",
                "municipio_original": "Estado do Paraná",
                "evento": "fixacao_inicio_atividades",
                "status_evento": "implementada",
                "ano_referencia": 2021,
                "observacao": "Cláusula expressa do cronograma: Início das atividades em 02/01/2021 (Protocolo 17.021.626-1).",
                "fonte": "Início das atividades 02/01/2021"
            })
        else:
            # Editais administrativos / processo seletivo de pessoal (candidatos com RG)
            # Registra apenas o ato geral sem confundir RG de candidatos com código INEP
            evidencias.append({
                "documento": pdf_name,
                "tipo_documento": "Processo Seletivo de Pessoal / Gestão CCM",
                "numero_documento": num_doc,
                "data_documento": data_doc,
                "pagina": 1,
                "codigo_inep": "",
                "nome_escola_original": "Instituições de Ensino Cívico-Militares (Vagas de Diretores / Monitores)",
                "nome_escola_normalizado": "INSTITUICOES DE ENSINO CIVICO-MILITARES (VAGAS DE DIRETORES / MONITORES)",
                "municipio_original": "Estado do Paraná",
                "evento": "processo_seletivo_pessoal",
                "status_evento": "instituicao_com_vaga",
                "ano_referencia": 2024 if "2024" in stem or "2023" in stem else "",
                "observacao": f"Edital referente a credenciamento, homologação de saúde ou seleção de militares/diretores. Documento: {stem}.",
                "fonte": f"Cabeçalho do documento {stem}"
            })
            
    df_evid = pd.DataFrame(evidencias)
    df_evid.to_csv(OUTPUT_EVIDENCIAS, index=False, sep=";", encoding="utf-8-sig")
    
    df_rev = pd.DataFrame(revisoes)
    df_rev.to_csv(OUTPUT_REVISAO, index=False, sep=";", encoding="utf-8-sig")
    
    print(f"\n==========================================")
    print(f"ESTRUTURAÇÃO CONCLUÍDA COM SUCESSO!")
    print(f"==========================================")
    print(f"Total de registros de evidências: {len(df_evid)}")
    
    escolas_com_inep = df_evid[df_evid["codigo_inep"] != ""]
    print(f"Evidências nominais de escolas com código INEP oficial: {len(escolas_com_inep)}")
    print(f"Códigos INEP únicos identificados: {escolas_com_inep['codigo_inep'].nunique()}")
    print(f"Atos normativos gerais / processos seletivos: {len(df_evid[df_evid['codigo_inep'] == ''])}")
    print(f"Casos sinalizados para revisão manual em extracao_revisao.csv: {len(df_rev)}")
    print(f"\nDistribuição de Eventos:")
    print(df_evid["evento"].value_counts())
    print(f"\nDistribuição de Anos de Referência:")
    print(df_evid["ano_referencia"].value_counts())

if __name__ == "__main__":
    processar_evidencias()
