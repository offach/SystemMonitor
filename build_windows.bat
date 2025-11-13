@echo off
REM Build script for Windows

echo Building SystemMonitor for Windows...

REM Check if PyInstaller is installed
where pyinstaller >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Build the application
echo Creating Windows executable...
pyinstaller --onefile ^
    --windowed ^
    --name SystemMonitor ^
    main.py

if exist "dist\SystemMonitor.exe" (
    echo Build successful! Executable is in dist\SystemMonitor.exe
) else (
    echo Build completed. Check dist\ directory for the executable.
)

echo Done!

