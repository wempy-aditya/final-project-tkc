@echo off
REM Script untuk setup awal proyek

REM Pindah ke direktori script
cd /d "%~dp0"

echo ========================================
echo Multimodal RAG System - Initial Setup
echo ========================================
echo.
echo Current directory: %CD%
echo.

REM Cek apakah venv sudah ada
echo [1/5] Checking virtual environment...
if exist "venv\Scripts\activate.bat" (
    echo Virtual environment found!
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Creating new one...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        echo Make sure Python is installed and in PATH
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
    call venv\Scripts\activate.bat
)

if errorlevel 1 (
    echo ERROR: Virtual environment not found
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
)

echo [2/5] Installing dependencies...
echo This may take 5-10 minutes...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo [3/5] Checking .env file...
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file and add your API keys!
    echo Press any key to open .env file in notepad...
    pause >nul
    notepad .env
)

echo.
echo [4/5] Setup complete!
echo.
echo ========================================
echo Next Steps:
echo ========================================
echo.
echo 1. Make sure you have added API keys to .env file
echo.
echo 2. To download dataset and generate embeddings (OPTIONAL):
echo    python scripts\setup.py
echo    (This will take 20-30 minutes and download ~2GB)
echo.
echo 3. To run the application:
echo    run.bat
echo    OR
echo    streamlit run src\ui\app.py
echo.
echo 4. For demo without backend:
echo    Open demo\index.html in your browser
echo.
echo ========================================

pause
