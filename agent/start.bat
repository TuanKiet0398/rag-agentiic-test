@echo off
echo 🎯 Agentic RAG System - Quick Start
echo ===================================

cd /d "%~dp0"

echo 📍 Current directory: %CD%

:: Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.10+ first.
    pause
    exit /b 1
)

echo ✅ Python found

:: Try Poetry first, then fallback to pip
echo 📦 Installing dependencies...

poetry --version >nul 2>&1
if %errorlevel% equ 0 (
    echo 🔧 Using Poetry...
    poetry install
    if %errorlevel% neq 0 (
        echo ❌ Poetry install failed
        goto :pip_fallback
    )
    echo ✅ Poetry installation complete
    goto :start_agent
) else (
    goto :pip_fallback
)

:pip_fallback
echo ⚠️ Poetry not found, using pip...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Pip install failed
    pause
    exit /b 1
)
echo ✅ Pip installation complete

:start_agent
echo 🚀 Starting Agentic RAG System...
python start.py

pause