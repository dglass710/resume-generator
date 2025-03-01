@echo off
REM Fetch latest changes from git and move to the head of your branch.
git fetch
git reset --hard origin/master

REM Build the executable with PyInstaller.
REM The --noconfirm flag tells PyInstaller to overwrite existing builds without asking.
pyinstaller --onefile --noconsole --noconfirm --add-data "data.json;." --add-data "default_data.json;." --add-data "generator.py;." ResumeBuilder.py

REM Clean up the temporary VBScript.
del sendkey.vbs
