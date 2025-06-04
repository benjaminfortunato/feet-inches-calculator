@echo off
echo Feet and Inches Calculator - Quick Start
echo ========================================
echo.

echo Installing dependencies...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo Running the calculator...
echo Close the calculator window when you're done testing.
python main.py

echo.
echo Calculator closed.
pause
