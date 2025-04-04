@echo off
REM Step 0: Update the repository by fetching the latest changes and hard-resetting to origin/main
git fetch origin && git reset --hard origin/main

REM Step 1: Build the executable using PyInstaller (auto-confirm overwrite)
pyinstaller --onefile --noconsole --noconfirm --add-data "data.json^;." --add-data "default_data.json^;." --add-data "generator.py^;." ResumeBuilder.py

REM Step 2: Copy the generated executable from the dist folder to the Executable directory
IF NOT EXIST Executable mkdir Executable
copy "dist\ResumeBuilder.exe" "Executable\ResumeBuilder.exe"

REM Step 3: Stage the updated executable for commit
git add "Executable\ResumeBuilder.exe"

REM Step 4: Commit the changes with a standardized message
git commit -m "Automated build: Updated ResumeBuilder.exe from the latest PyInstaller build"

REM Step 5: Optional: Push the changes to the remote repository
REM Uncomment the following line if you want to auto-push the commit:
git push

REM Step 6: Install locally by copying the executable to the designated folder
IF NOT EXIST "C:\Program Files\Resume Generator\" mkdir "C:\Program Files\Resume Generator\"
copy "dist\ResumeBuilder.exe" "C:\Program Files\Resume Generator\"
