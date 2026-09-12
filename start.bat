@echo off
echo ========================================
echo VOID - Starting Application
echo Created by Yinuo
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [!] Virtual environment not found
    echo [*] Running setup...
    call setup.bat
    if %errorlevel% neq 0 (
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the application
echo [*] Starting Void dashboard...
python main.py

REM Keep window open if there's an error
if %errorlevel% neq 0 (
    echo.
    echo [!] Application exited with error code %errorlevel%
    pause
)