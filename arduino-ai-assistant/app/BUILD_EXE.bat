@echo off
cd /d "%~dp0"
echo Installing build tools...
python -m pip install -r requirements.txt pyinstaller
if errorlevel 1 (echo. & echo Python is missing. Install it from python.org and tick "Add python.exe to PATH". & pause & exit /b 1)
echo Building AI-Assistant.exe ...
python -m PyInstaller --noconfirm --onefile --windowed --name AI-Assistant --collect-data customtkinter --collect-all sounddevice ai_assistant_app.py
if errorlevel 1 (echo Build failed - send a screenshot of this window. & pause & exit /b 1)
copy /y dist\AI-Assistant.exe "%~dp0AI-Assistant.exe" >nul
echo.
echo DONE! AI-Assistant.exe is in this folder.
explorer /select,"%~dp0AI-Assistant.exe"
pause
