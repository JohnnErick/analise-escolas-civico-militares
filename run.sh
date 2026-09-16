#!/usr/bin/env bash
# Script para iniciar o Painel de Análise de Escolas Cívico-Militares

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ ! -d ".venv" ]; then
    echo "Ambiente virtual não encontrado. Criando..."
    python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt
fi

echo "Iniciando o Painel Streamlit..."
.venv/bin/streamlit run app.py
