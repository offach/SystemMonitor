#!/bin/bash

# Build script for macOS
echo "Building SystemMonitor for macOS..."

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "Installing PyInstaller..."
    pip install pyinstaller
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Build the application as .app bundle
echo "Creating macOS application..."
pyinstaller --windowed \
    --name SystemMonitor \
    --icon=NONE \
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

