@echo off
title Weatherly - Build Executable
echo ============================================================
echo   Compiling Weatherly Standalone Executable
echo ============================================================
echo.

pip install pyinstaller customtkinter requests Pillow
pyinstaller --noconsole --onefile --name Weatherly weatherapp.py

echo.
echo ============================================================
echo   Build Completed!
echo   Standalone binary is saved in: dist\Weatherly.exe
echo ============================================================
pause
