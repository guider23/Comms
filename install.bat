@echo off
echo Installing Comment Removal Tool...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Python found. Installing package...
pip install -e .

if errorlevel 1 (
    echo.
    echo ERROR: Installation failed
    pause
    exit /b 1
)

echo.
echo SUCCESS: Comment Removal Tool installed!
echo.
echo Usage:
echo   python -m comms.cli --help
echo   python -m comms.cli [directory]
echo   python -m comms.cli --demo
echo.
pause
