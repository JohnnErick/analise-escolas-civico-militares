"""
Script de Extração Literal Página a Página dos Editais.
Gera para cada arquivo PDF em 'biblioteca de ref/editais/' um arquivo .txt correspondente
em 'data/extracted/editais/', demarcando explicitamente cada página para garantir rastreabilidade estrita.
Preserva rigorosamente a grafia original, quebras de linha e estrutura literal do documento.
"""

from pathlib import Path
from pypdf import PdfReader

BASE_DIR = Path(__file__).resolve().parent.parent
EDITAIS_DIR = BASE_DIR / "biblioteca de ref" / "editais"
OUTPUT_DIR = BASE_DIR / "data" / "extracted" / "editais"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def extrair_todos():
    arquivos = sorted(list(EDITAIS_DIR.glob("*.pdf")))
    print(f"Iniciando extração literal de {len(arquivos)} arquivos PDF...")
    
    total_sucesso = 0
    total_erros = 0
    total_paginas = 0
    
    for idx, arq in enumerate(arquivos, start=1):
        txt_filename = arq.stem + ".txt"
        out_path = OUTPUT_DIR / txt_filename
        
        try:
            reader = PdfReader(arq)
            qtd_pag = len(reader.pages)
            total_paginas += qtd_pag
            
            with open(out_path, "w", encoding="utf-8") as f_out:
                f_out.write(f"DOCUMENTO_FONTE: {arq.name}\n")
                f_out.write(f"TOTAL_PAGINAS: {qtd_pag}\n")
                f_out.write("=" * 60 + "\n\n")
                
                for num_pag, page in enumerate(reader.pages, start=1):
                    f_out.write(f"=== PÁGINA {num_pag} ===\n")
                    texto_pag = page.extract_text() or ""
                    f_out.write(texto_pag)
                    f_out.write(f"\n=== FIM PÁGINA {num_pag} ===\n\n")
                    
            total_sucesso += 1
            if idx % 10 == 0 or idx == len(arquivos):
                print(f"[{idx}/{len(arquivos)}] Processado: {arq.name} ({qtd_pag} págs)")
        except Exception as e:
            print(f"[ERRO] Falha ao extrair {arq.name}: {e}")
            total_erros += 1
            
    print(f"\nExtração concluída!")
    print(f"Sucesso: {total_sucesso} arquivos ({total_paginas} páginas no total)")
    print(f"Erros: {total_erros}")
    print(f"Diretório de saída: {OUTPUT_DIR}")

if __name__ == "__main__":
    extrair_todos()
