#!/bin/bash

# Detect OS and set the appropriate separator for PyInstaller
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Building for macOS..."
    SEPARATOR=":"
    OUTPUT="ResumeBuilder.app"
else
    # Windows
    echo "Building for Windows..."
    SEPARATOR=";"
    OUTPUT="ResumeBuilder.exe"
fi

# Build with the correct separator
pyinstaller --onefile --noconsole --noconfirm \
    --add-data "default_data.json${SEPARATOR}." \
    --add-data "generator.py${SEPARATOR}." \
    ResumeBuilder.py

# Handle OS-specific post-build steps
if [[ "$OSTYPE" == "darwin"* ]]; then
    # Zip and move the .app
    zip -r Executable/ResumeBuilder.zip dist/ResumeBuilder.app
    git add Executable/ResumeBuilder.zip
    
    # Install locally if desired
    read -p "Install to Applications folder? (y/n) " -n 1 -r
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp -r dist/ResumeBuilder.app /Applications/
    fi
else
    # Move the Windows executable
    mkdir -p Executable
    cp "dist/ResumeBuilder.exe" "Executable/ResumeBuilder.exe"
    git add "Executable/ResumeBuilder.exe"
fi

# Commit and optionally push
git commit -m "Automated build: Updated ResumeBuilder for $(uname -s)"

read -p "Push to remote? (y/n) " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git push origin main
fi
