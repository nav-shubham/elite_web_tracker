@echo off
:: Navigate to the script's directory
cd /d "%~dp0"

:: 1. Activate the Virtual Environment
echo [SYSTEM] Activating Virtual Environment...
call venv\Scripts\activate

:: 2. Launch Uvicorn with Auto-Reload
echo [SYSTEM] Starting FastAPI Server on http://127.0.0.1:8000
uvicorn main:app --reload