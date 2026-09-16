#!/bin/bash
# ==============================================================================
# Painel de Análise de Escolas Cívico-Militares do Paraná
# Inicializador Automático de 1 Clique para macOS (MacBook)
# ==============================================================================

# 1. Garante que o diretório de execução seja a pasta onde este arquivo está
cd "$(dirname "$0")"

echo "=================================================================="
echo "    📊 Painel de Análise de Escolas do Paraná (SEED / INEP)       "
echo "=================================================================="
echo ""

# 2. Localização do Python 3 no macOS
if command -v python3 >/dev/null 2>&1; then
    PY_BIN="python3"
elif [ -f "/opt/homebrew/bin/python3" ]; then
    PY_BIN="/opt/homebrew/bin/python3"
elif [ -f "/usr/local/bin/python3" ]; then
    PY_BIN="/usr/local/bin/python3"
elif [ -f "/usr/bin/python3" ]; then
    PY_BIN="/usr/bin/python3"
else
    echo "❌ Ops! Não encontramos o Python 3 instalado no seu MacBook."
    echo ""
    echo "💡 Como resolver rapidamente (apenas uma vez):"
    echo "   Abra o aplicativo Terminal e cole o comando:"
    echo "   xcode-select --install"
    echo ""
    echo "   Ou baixe o instalador oficial em: https://www.python.org/downloads/"
    echo ""
    read -p "Pressione [ENTER] para fechar..."
    exit 1
fi

# 3. Configuração automática do ambiente virtual na primeira execução
if [ ! -d ".venv" ]; then
    echo "⏳ Configurando o painel pela primeira vez..."
    echo "   (Instalando bibliotecas necessárias. Isso leva cerca de 1 minuto)..."
    echo ""
    "$PY_BIN" -m venv .venv
    .venv/bin/pip install --upgrade pip --quiet
    .venv/bin/pip install -r requirements.txt --quiet
    echo "✅ Instalação concluída com sucesso!"
    echo ""
fi

# 4. Iniciação do painel e abertura automática do navegador
echo "🚀 Abrindo o painel no seu navegador de internet..."
echo "💡 Dica: Para encerrar o painel, basta fechar esta janela do Terminal."
echo ""

.venv/bin/streamlit run app.py --server.headless false
