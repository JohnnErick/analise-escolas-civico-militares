"""
Script de Inventário Documental dos Colégios Cívico-Militares do Paraná.
Varre a pasta 'biblioteca de ref/editais' e gera um relatório detalhado em CSV
com as características técnicas de cada documento (páginas, texto nativo, tabelas, etc.).
"""

import os
import re
from pathlib import Path
import pandas as pd
from pypdf import PdfReader

BASE_DIR = Path(__file__).resolve().parent.parent
EDITAIS_DIR = BASE_DIR / "biblioteca de ref" / "editais"
OUTPUT_CSV = BASE_DIR / "data" / "validation" / "inventario_documentos.csv"
OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

def classificar_tipo_provavel(nome: str, texto_amostra: str) -> str:
    n_lower = nome.lower()
    t_lower = texto_amostra.lower()
    
    if "resultado" in n_lower or "resultado" in t_lower:
        if "consulta" in n_lower or "consulta" in t_lower:
            return "Resultado de Consulta Pública"
        elif "investigacao" in n_lower or "saude" in n_lower or "final" in n_lower:
            return "Resultado de Etapa de Processo Seletivo"
        return "Edital de Resultado"
    elif "consulta_publica" in n_lower or "consulta publica" in t_lower:
        return "Edital de Convocação para Consulta Pública"
    elif "cronograma" in n_lower or "retifica" in n_lower or "prorrogar" in n_lower:
        return "Retificação de Cronograma / Prorrogação"
    elif "processo_seletivo" in n_lower or "pss" in n_lower or "cmeiv" in n_lower or "credenciamento" in t_lower:
        return "Processo Seletivo de Pessoal / Militares da Reserva (CMEIV)"
    elif "expansao" in n_lower:
        return "Edital de Expansão do Programa"
    elif "altera" in n_lower:
        return "Edital de Alteração de Normativa"
    elif "edital" in n_lower:
        return "Edital Administrativo / Diversos"
    else:
        return "Documento Administrativo"

def detectar_provavel_lista_escolas(texto: str) -> bool:
    t_lower = texto.lower()
    termos = [
        "cód. mec", "cod. mec", "código inep", "município", "estabelecimento",
        "instituição de ensino", "anexo do edital", "anexo i", "anexo ii",
        "relação das instituições", "instituições de ensino elencadas"
    ]
    matches = sum(1 for termo in termos if termo in t_lower)
    return matches >= 2

def detectar_tabelas(texto: str) -> bool:
    # Procura padrões tabulares comuns (linhas repetidas com dígitos seguidos de nomes em caixa alta e quebras)
    linhas = texto.split("\n")
    linhas_com_codigo = sum(1 for l in linhas if re.search(r"\b41\d{6}\b", l))
    return linhas_com_codigo >= 2

def inventariar():
    arquivos = sorted(list(EDITAIS_DIR.glob("*.pdf")))
    print(f"Iniciando inventário de {len(arquivos)} arquivos PDF em {EDITAIS_DIR}...")
    
    registros = []
    
    for arq in arquivos:
        tam = arq.stat().st_size
        nome = arq.name
        
        try:
            reader = PdfReader(arq)
            qtd_pag = len(reader.pages)
            
            # Amostra de texto e inspeção das páginas
            texto_completo = ""
            tem_imagem = False
            
            for pag in reader.pages:
                t = pag.extract_text() or ""
                texto_completo += t + "\n"
                if not tem_imagem and len(pag.images) > 0:
                    tem_imagem = True
                    
            texto_limpo = texto_completo.strip()
            possui_texto = len(texto_limpo) > 50
            pdf_nativo = possui_texto  # Se possui texto selecionável sem OCR
            
            tem_lista = detectar_provavel_lista_escolas(texto_completo)
            tem_tabela = detectar_tabelas(texto_completo)
            tipo = classificar_tipo_provavel(nome, texto_completo[:1000])
            
            registros.append({
                "nome_arquivo": nome,
                "caminho_relativo": str(arq.relative_to(BASE_DIR)),
                "extensao": arq.suffix.lower(),
                "tamanho_bytes": tam,
                "qtd_paginas": qtd_pag,
                "pdf_nativo": pdf_nativo,
                "possui_texto_selecionavel": possui_texto,
                "possui_tabelas_detectadas": tem_tabela,
                "possui_imagens": tem_imagem,
                "contem_lista_escolas_provavel": tem_lista,
                "tipo_provavel": tipo
            })
        except Exception as e:
            registros.append({
                "nome_arquivo": nome,
                "caminho_relativo": str(arq.relative_to(BASE_DIR)),
                "extensao": arq.suffix.lower(),
                "tamanho_bytes": tam,
                "qtd_paginas": None,
                "pdf_nativo": False,
                "possui_texto_selecionavel": False,
                "possui_tabelas_detectadas": False,
                "possui_imagens": False,
                "contem_lista_escolas_provavel": False,
                "tipo_provavel": f"Erro de leitura: {e}"
            })
            
    df_inv = pd.DataFrame(registros)
    df_inv.to_csv(OUTPUT_CSV, index=False, sep=";", encoding="utf-8-sig")
    print(f"Inventário concluído com sucesso!")
    print(f"Arquivo salvo em: {OUTPUT_CSV}")
    print(f"Total documentos inventariados: {len(df_inv)}")
    print(f"Documentos com provável lista de escolas: {df_inv['contem_lista_escolas_provavel'].sum()}")
    print("\nDistribuição de tipos:")
    print(df_inv["tipo_provavel"].value_counts())

if __name__ == "__main__":
    inventariar()
