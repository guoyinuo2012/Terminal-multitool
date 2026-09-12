@echo off
echo ========================================
echo VOID - Installation Script
echo Created by Yinuo
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python is not installed or not in PATH
    echo [*] Running Python installer...
    call python_installer.bat
    if %errorlevel% neq 0 (
        echo [!] Python installation failed
        pause
        exit /b 1
    )
) else (
    echo [+] Python is installed
    python --version
)

echo.
echo [*] Creating virtual environment...
python -m venv venv

echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

echo [*] Installing required packages...
pip install --upgrade pip
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [!] Failed to install requirements
    pause
    exit /b 1
)

echo.
echo [+] Installation completed successfully!
echo [*] Run 'start.bat' to launch the application
echo.
pause