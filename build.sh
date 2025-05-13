#!/bin/bash

# Function to show help message
show_help() {
    echo "Usage: ./build.sh [options]"
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  --amend       Amend to previous commit (for adding macOS build)"
    echo "  --install     Install locally after building (macOS only)"
}

# Parse command line arguments
AMEND=false
INSTALL=false
for arg in "$@"; do
    case $arg in
        -h|--help)
            show_help
            exit 0
            ;;
        --amend)
            AMEND=true
            ;;
        --install)
            INSTALL=true
            ;;
    esac
done

# Detect OS and set the appropriate separator for PyInstaller
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Building for macOS..."
    SEPARATOR=":"
    OUTPUT="ResumeBuilder.app"
    COMMIT_MSG="build: update macOS app bundle"
else
    # Windows
    echo "Building for Windows..."
    SEPARATOR=";"
    OUTPUT="ResumeBuilder.exe"
    COMMIT_MSG="build: update Windows executable"
fi

# Build with the correct separator
pyinstaller --onefile --noconsole --noconfirm \
    --add-data "default_data.json${SEPARATOR}." \
    --add-data "generator.py${SEPARATOR}." \
    ResumeBuilder.py

# Handle OS-specific post-build steps
if [[ "$OSTYPE" == "darwin"* ]]; then
    # Zip and move the .app
    mkdir -p Executable
    zip -r Executable/ResumeBuilder.zip dist/ResumeBuilder.app
    git add Executable/ResumeBuilder.zip
    
    # Install locally if requested
    if [[ "$INSTALL" == true ]]; then
        echo "Installing to Applications folder..."
        cp -r dist/ResumeBuilder.app /Applications/
    fi
else
    # Move the Windows executable
    mkdir -p Executable
    cp "dist/ResumeBuilder.exe" "Executable/ResumeBuilder.exe"
    git add "Executable/ResumeBuilder.exe"
fi

# Handle commit and push
if [[ "$AMEND" == true ]]; then
    echo "\nAmending previous commit with macOS build..."
    git commit --amend --no-edit
    git push --force-with-lease origin main
else
    echo "\nCommitting build..."
    git commit -m "$COMMIT_MSG"
    git push origin main
fi
