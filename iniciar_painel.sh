#!/bin/bash
# ==============================================================================
# Painel de Análise de Escolas Cívico-Militares do Paraná
# Inicializador Automático para Linux / macOS via Terminal
# ==============================================================================

cd "$(dirname "$0")"

echo "=================================================================="
echo "    📊 Painel de Análise de Escolas do Paraná (SEED / INEP)       "
echo "=================================================================="
echo ""

if command -v python3 >/dev/null 2>&1; then
    PY_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PY_BIN="python"
else
    echo "❌ Python não encontrado. Por favor instale o Python 3."
    exit 1
fi

if [ ! -d ".venv" ]; then
    echo "⏳ Configurando o ambiente pela primeira vez..."
    "$PY_BIN" -m venv .venv
    .venv/bin/pip install --upgrade pip --quiet
    .venv/bin/pip install -r requirements.txt --quiet
    echo "✅ Instalação concluída!"
    echo ""
fi

echo "🚀 Iniciando painel no navegador..."
.venv/bin/streamlit run app.py --server.headless false
