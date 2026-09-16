@echo off
chcp 65001 >nul
title Painel de Análise de Escolas do Paraná

echo ==================================================================
echo     📊 Painel de Análise de Escolas do Paraná (SEED / INEP)       
echo ==================================================================
echo.

cd /d "%~dp0"

where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    set "PY_CMD=py"
) else (
    where python >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        set "PY_CMD=python"
    ) else (
        echo ❌ Python não foi encontrado no seu computador.
        echo.
        echo 💡 Por favor, instale o Python pela Microsoft Store ou em:
        echo    https://www.python.org/downloads/
        echo    (Lembre-se de marcar a opção "Add Python to PATH")
        echo.
        pause
        exit /b 1
    )
)

if not exist ".venv" (
    echo ⏳ Configurando o painel pela primeira vez...
    echo    (Isso pode levar de 1 a 2 minutos)...
    echo.
    %PY_CMD% -m venv .venv
    call .venv\Scripts\python.exe -m pip install --upgrade pip --quiet
    call .venv\Scripts\python.exe -m pip install -r requirements.txt --quiet
    echo ✅ Instalação concluída com sucesso!
    echo.
)

echo 🚀 Abrindo o painel no seu navegador de internet...
echo 💡 Dica: Para encerrar o painel, basta fechar esta janela.
echo.

call .venv\Scripts\streamlit.exe run app.py
pause
