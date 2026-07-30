@echo off
setlocal
cd /d "%~dp0"

where uv >nul 2>&1
if errorlevel 1 goto uv_not_found

uv run --isolated --no-project --python ">=3.10" --with-requirements requirements.txt build.py
if errorlevel 1 goto build_failed

uv cache prune
if errorlevel 1 goto build_failed

echo.
echo Build completed: dist\PhotoLocationMap.exe
pause
exit /b 0

:uv_not_found
echo.
echo ERROR: uv was not found.
echo Install it with: winget install --id Astral-sh.uv
echo Then open a new command prompt and run this file again.
goto build_failed

:build_failed
echo.
echo Build failed.
pause
exit /b 1
