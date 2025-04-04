@echo off
REM Step 0: Update the repository by fetching the latest changes and hard-resetting to origin/main
git fetch origin && git reset --hard origin/main

REM Step 1: Build the executable using PyInstaller (auto-confirm overwrite)
pyinstaller --onefile --noconsole --noconfirm --add-data "data.json;." --add-data "default_data.json;." --add-data "generator.py;." ResumeBuilder.py

REM Step 2: Zip the generated executable into the Executable directory
REM Note: On Windows, PyInstaller produces an .exe in the "dist" folder.
IF NOT EXIST Executable mkdir Executable
powershell -Command "Compress-Archive -Path dist\ResumeBuilder.exe -DestinationPath Executable\ResumeBuilder.zip -Force"

REM Step 3: Stage the updated ZIP file for commit
git add Executable\ResumeBuilder.zip

REM Step 4: Commit the changes with a standardized message
git commit -m "Automated build: Updated ResumeBuilder.zip from the latest PyInstaller build"

REM Step 5: Optional: Push the changes to the remote repository
REM Uncomment the next line if you want to auto-push the commit to your remote repository
git push
