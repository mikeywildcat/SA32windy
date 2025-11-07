@echo off
echo ========================================
echo  Universal Windows Build Script
echo ========================================
echo.

REM Detect system architecture
echo Detecting system architecture...
wmic cpu get caption | findstr /i "ARM" >nul
if %errorlevel% equ 0 (
    echo System: ARM64
    set ARCH=ARM64
) else (
    echo System: x64/x86
    set ARCH=x64
)

echo.
echo NOTE: This executable will ONLY work on %ARCH% systems.
echo.
echo To support ALL Windows users:
echo   1. Build on ARM64 Windows for ARM64 users
echo   2. Build on x64 Windows for x64/x86 users
echo   3. Distribute both versions
echo.
echo Alternatively, distribute the Python script instead!
echo.

REM Clean previous builds
if exist build rd /s /q build
if exist dist rd /s /q dist
if exist SailawayWindyBridge.spec del SailawayWindyBridge.spec

echo Building standalone executable for %ARCH%...
echo.

pyinstaller --onefile --windowed --name "SailawayWindyBridge_%ARCH%" sailaway_to_windy.py

echo.
if exist "dist\SailawayWindyBridge_%ARCH%.exe" (
    echo ========================================
    echo  Build completed successfully!
    echo ========================================
    echo.
    echo Executable created: dist\SailawayWindyBridge_%ARCH%.exe
    echo.
    echo WARNING: This .exe only works on %ARCH% Windows systems!
    echo.
    echo For universal distribution, consider:
    echo   - Building on both ARM64 and x64 systems
    echo   - Or sharing the Python script instead
    echo.
) else (
    echo ========================================
    echo  Build failed!
    echo ========================================
    echo.
)

pause
