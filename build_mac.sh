#!/bin/bash

# Build script for macOS
echo "Building SystemMonitor for macOS..."

# Detect pip command
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v python3 -m pip &> /dev/null; then
    PIP_CMD="python3 -m pip"
else
    PIP_CMD="pip"
fi

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "Installing PyInstaller..."
    $PIP_CMD install pyinstaller
fi

# Install dependencies
echo "Installing dependencies..."
$PIP_CMD install -r requirements.txt

# Build the application as .app bundle
echo "Creating macOS application..."
pyinstaller --windowed \
    --name SystemMonitor \
    --clean \
    main.py

if [ -d "dist/SystemMonitor.app" ]; then
    echo "Build successful! Application is in dist/SystemMonitor.app"
    echo "You can also create a one-file executable by running:"
    echo "  pyinstaller --onefile --windowed --name SystemMonitor main.py"
else
    echo "Build completed. Check dist/ directory for the executable."
fi

echo "Done!"

