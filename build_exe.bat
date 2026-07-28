@echo off
chcp 65001 >nul
title Nova Wallet - build EXE
cd /d "%~dp0"

echo ============================================
echo   Nova Wallet - sborka EXE (Windows)
echo ============================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
  echo [!] Python ne nayden. Ustanovi Python 3 s python.org
  echo     i obyazatelno postav galochku "Add python.exe to PATH".
  pause
  exit /b 1
)

echo [1/2] Ustanovka PyInstaller...
python -m pip install --upgrade pyinstaller >nul
if errorlevel 1 (
  echo [!] Ne udalos ustanovit PyInstaller. Proveri internet.
  pause
  exit /b 1
)

echo [2/2] Sborka NovaWallet.exe...
python -m PyInstaller --onefile --noconsole --name NovaWallet ^
  --add-data "CryptoWallet.html;." wallet.py
if errorlevel 1 (
  echo [!] Oshibka sborki.
  pause
  exit /b 1
)

echo.
echo Gotovo! Fayl: %~dp0dist\NovaWallet.exe
echo Mozhesh perenesti ego kuda ugodno - on samodostatochnyy.
pause
