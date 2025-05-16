#!/bin/bash

# Define the source and destination paths
SOURCE="Executable/ResumeBuilder.zip"
DESTINATION="/Applications"

# Function to calculate checksums of the existing app
calculate_checksums() {
    find "$1" -type f -exec shasum {} \; | sort | shasum
}

# Unzip the ResumeBuilder.zip into a temporary directory
TEMP_DIR="/tmp/ResumeBuilder"
mkdir -p "$TEMP_DIR"
unzip -o "$SOURCE" -d "$TEMP_DIR"

# Calculate checksums for the existing app and the new app
EXISTING_CHECKSUM=$(calculate_checksums "$DESTINATION/dist/ResumeBuilder.app")
NEW_CHECKSUM=$(calculate_checksums "$TEMP_DIR/dist/ResumeBuilder.app")

# Compare checksums
if [ "$EXISTING_CHECKSUM" == "$NEW_CHECKSUM" ]; then
    echo "No changes detected. Skipping installation."
    rm -rf "$TEMP_DIR"
    exit 0
fi

# Copy the new app to the Applications folder
cp -r "$TEMP_DIR/dist/ResumeBuilder.app" "$DESTINATION/dist/"

# Confirm the installation
if [ -d "$DESTINATION/dist/ResumeBuilder.app" ]; then
    echo "ResumeBuilder installed successfully in $DESTINATION/dist/"
else
    echo "Installation failed."
fi

# Clean up
rm -rf "$TEMP_DIR"
