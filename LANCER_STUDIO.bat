@echo off
cd /d "%~dp0"
py -3 studio_prive.py
if errorlevel 1 python studio_prive.py
pause
