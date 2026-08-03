@echo off
REM ============================================================
REM  One-click build for YT Downloader (.exe)
REM  Double-click this file. It installs what it needs, then
REM  produces dist\YT-Downloader.exe
REM ============================================================
setlocal
cd /d "%~dp0"

echo.
echo [1/3] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python was not found on PATH.
    echo Install Python 3.10+ from https://www.python.org/downloads/
    echo and tick "Add Python to PATH" during setup.
    pause
    exit /b 1
)

echo.
echo [2/3] Installing dependencies (PyQt6, yt-dlp, PyInstaller)...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt pyinstaller
if errorlevel 1 (
    echo ERROR: Dependency install failed.
    pause
    exit /b 1
)

echo.
echo [3/3] Building the executable...
python -m PyInstaller --noconfirm YT-Downloader.spec
if errorlevel 1 (
    echo ERROR: Build failed.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  Done!  Your app is at:  dist\YT-Downloader.exe
echo.
echo  NOTE: MP3 conversion needs ffmpeg. Either:
echo    - install ffmpeg and add it to PATH, OR
echo    - drop ffmpeg.exe next to this .bat and rebuild, OR
echo    - keep ffmpeg.exe next to dist\YT-Downloader.exe
echo ============================================================
echo.
pause
