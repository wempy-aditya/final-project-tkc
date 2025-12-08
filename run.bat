@echo off
REM Script untuk aktivasi virtual environment dan menjalankan Streamlit

REM Pindah ke direktori script
cd /d "%~dp0"

echo ========================================
echo Multimodal RAG System - Quick Start
echo ========================================
echo.
echo Current directory: %CD%
echo.

REM Aktivasi virtual environment
echo [1/3] Activating virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

REM Check if activation successful
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

echo [2/3] Virtual environment activated!
echo.

REM Check if dependencies installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Dependencies not found. Installing...
    echo This may take several minutes...
    pip install --upgrade pip
    pip install -r requirements.txt
    echo.
    echo [3/3] Dependencies installed!
) else (
    echo [3/3] Dependencies already installed
)

echo.
echo ========================================
echo Starting Streamlit application...
echo ========================================
echo.
echo The app will open in your browser at:
echo http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Run Streamlit
streamlit run src\ui\app.py

pause
