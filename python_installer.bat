@echo off
echo ========================================
echo Python Installer Helper
echo ========================================
echo.

echo [*] This script will help you install Python 3.11+
echo.
echo Please download Python 3.11 or higher from:
echo https://www.python.org/downloads/
echo.
echo IMPORTANT: During installation, check the box:
echo "Add Python to PATH"
echo.

echo Press any key to open the Python download page...
pause >nul

start https://www.python.org/downloads/

echo.
echo [*] After installing Python, press any key to continue...
pause >nul

REM Verify Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python still not found in PATH
    echo [*] Please restart your command prompt after installation
    echo [*] Or manually add Python to your system PATH
    pause
    exit /b 1
) else (
    echo [+] Python successfully installed!
    python --version
    exit /b 0
)