#!/bin/bash

# Step 1: Build the executable using PyInstaller (auto-confirm overwrite)
yes | pyinstaller --onefile --noconsole --add-data "data.json:." --add-data "default_data.json:." --add-data "generator.py:." ResumeBuilder.py

# Step 2: Zip the generated .app file into the Executable directory
zip -r Executable/ResumeBuilder.zip dist/ResumeBuilder.app

# Step 3: Stage the updated ZIP file for commit
git add Executable/ResumeBuilder.zip

# Step 4: Commit the changes with a standardized message
git commit -m "Automated build: Updated ResumeBuilder.zip from the latest PyInstaller build"

# Optional: Push the changes to the remote repository
# Uncomment the next line if you want to auto-push
git push

# Step 6: Install the new version locally 
cp -r dist/ResumeBuilder.app /Applications/
