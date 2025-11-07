@echo off
echo ========================================
echo  Building Sailaway to Windy GPS Bridge
echo ========================================
echo.

REM Clean previous builds
if exist build rd /s /q build
if exist dist rd /s /q dist
if exist sailaway_to_windy.spec del sailaway_to_windy.spec

echo Building standalone executable...
echo.

pyinstaller --onefile --windowed --name "SailawayWindyBridge" --icon=NONE sailaway_to_windy.py

echo.
if exist "dist\SailawayWindyBridge.exe" (
    echo ========================================
    echo  Build completed successfully!
    echo ========================================
    echo.
    echo Executable created: dist\SailawayWindyBridge.exe
    echo.
    echo You can now distribute the file:
    echo   dist\SailawayWindyBridge.exe
    echo.
    echo It contains everything needed to run the app!
    echo No Python installation required.
    echo.
) else (
    echo ========================================
    echo  Build failed!
    echo ========================================
    echo.
    echo Please check the error messages above.
    echo.
)

pause
