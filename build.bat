@echo off
echo Building Feet and Inches Calculator Executable
echo ===============================================
echo.

echo Installing dependencies and building executable...
python build.py

if %errorlevel% equ 0 (
    echo.
    echo Build completed successfully!
    echo You can find the executable in the 'dist' folder.
    echo.
    echo Would you like to run the executable now? (y/n)
    set /p choice=
    if /i "%choice%"=="y" (
        if exist "dist\FeetInchesCalculator.exe" (
            start "" "dist\FeetInchesCalculator.exe"
        ) else (
            echo Executable not found in dist folder.
        )
    )
) else (
    echo Build failed! Check the error messages above.
)

echo.
pause
