@echo off
setlocal
cd /d "%~dp0"

where uv >nul 2>&1
if errorlevel 1 goto uv_not_found

uv run --isolated --no-project --python ">=3.10" --with-requirements requirements.txt build.py
if errorlevel 1 goto build_failed

if not exist "dist\PhotoLocationMap.exe" goto output_not_found
copy /y "dist\PhotoLocationMap.exe" "PhotoLocationMap.exe" >nul
if errorlevel 1 goto build_failed

rmdir /s /q "build"
rmdir /s /q "build-spec"
rmdir /s /q "dist"
rmdir /s /q "__pycache__"
if exist "build" goto cleanup_failed
if exist "build-spec" goto cleanup_failed
if exist "dist" goto cleanup_failed
if exist "__pycache__" goto cleanup_failed

uv cache prune
if errorlevel 1 goto build_failed

echo.
echo Build completed: PhotoLocationMap.exe
pause
exit /b 0

:output_not_found
echo.
echo ERROR: dist\PhotoLocationMap.exe was not found.
goto build_failed

:cleanup_failed
echo.
echo ERROR: One or more build folders could not be removed.
goto build_failed

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
