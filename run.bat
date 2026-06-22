@echo off
title Speakr Launcher
cd /d "%~dp0"

REM --- Find Python installation (bypass Windows Store stub) ---
set PYTHON=

REM Known install location (most common)
if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" set "PYTHON=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PYTHON=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if exist "C:\Program Files\Python313\python.exe" set "PYTHON=C:\Program Files\Python313\python.exe"
if exist "C:\Program Files\Python312\python.exe" set "PYTHON=C:\Program Files\Python312\python.exe"

REM Fallback to py launcher if available
if "%PYTHON%"=="" (
    where py >nul 2>nul
    if not errorlevel 1 set PYTHON=py
)

REM Last resort: try python command directly
if "%PYTHON%"=="" (
    python --version >nul 2>nul
    if not errorlevel 1 set PYTHON=python
)

if "%PYTHON%"=="" (
    echo [ERROR] Python 3 not found.
    echo Please install Python 3 from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Using: %PYTHON%

REM --- Create virtual environment if needed ---
if not exist ".venv\Scripts\python.exe" (
    echo [1/3] Creating virtual environment...
    %PYTHON% -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
)

REM --- Install dependencies ---
echo [2/3] Installing dependencies...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)

pip install -q -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

REM --- Launch app ---
echo [3/3] Starting Speakr...
echo.
echo ============================================================
echo  Speakr is starting. Keep this window open to see debug logs.
echo  Close this window OR press Ctrl+C to stop Speakr.
echo  Hotkey: Ctrl + Shift + M
echo ============================================================
echo.

.venv\Scripts\python speakr_app.py
if errorlevel 1 (
    echo [ERROR] Speakr exited with error code %errorlevel%.
    pause
    exit /b 1
)

echo Speakr has exited.
pause