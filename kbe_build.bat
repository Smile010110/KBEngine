@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set "PROJECT_ROOT=%~dp0"
set "LOG_FILE=%PROJECT_ROOT%build.log"

echo ========================================= > "%LOG_FILE%"
echo KBEngine-Nex Build Log >> "%LOG_FILE%"
echo Start Time: %date% %time% >> "%LOG_FILE%"
echo ========================================= >> "%LOG_FILE%"

REM =========================================
REM 1. VS Environment Detection
REM =========================================
echo [Check] Finding Visual Studio...
set "VSWHERE_PATH=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"
if not exist "%VSWHERE_PATH%" (
    echo [ERROR] vswhere.exe not found >> "%LOG_FILE%"
    echo [ERROR] Please install VS2019+ or Build Tools
    pause
    exit /b 1
)

for /f "usebackq tokens=*" %%i in (`"%VSWHERE_PATH%" -latest -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath`) do (
    set "VS_INSTALL_PATH=%%i"
)

if not defined VS_INSTALL_PATH (
    echo [ERROR] C++ toolset not found >> "%LOG_FILE%"
    echo [ERROR] Please install "Desktop development with C++" component
    pause
    exit /b 1
)

echo [SUCCESS] VS Path: %VS_INSTALL_PATH%

REM =========================================
REM 2. Load VC Environment
REM =========================================
echo Loading VC build environment...
call "%VS_INSTALL_PATH%\VC\Auxiliary\Build\vcvarsall.bat" x64
if %errorlevel% neq 0 (
    echo [ERROR] VC environment failed! Code: %errorlevel% >> "%LOG_FILE%"
    echo [ERROR] Check VC components installation
    pause
    exit /b 1
)

where msbuild >nul
if %errorlevel% neq 0 (
    echo [ERROR] MSBuild not found >> "%LOG_FILE%"
    echo [ERROR] Check VS installation integrity
    pause
    exit /b 1
)

REM =========================================
REM 3. Build Projects
REM =========================================
set "PYTHON_BUILD_PROJ=%PROJECT_ROOT%kbe\src\lib\pythonBuild\pythonBuild.vcxproj"
set "SOLUTION_FILE=%PROJECT_ROOT%kbe\src\kbengine nex.sln"

echo Building Python component...
msbuild "%PYTHON_BUILD_PROJ%" /p:Configuration=Release /p:Platform=x64 /m >> "%LOG_FILE%" 2>&1
if %errorlevel% neq 0 goto build_failed

echo Building main solution...
msbuild "%SOLUTION_FILE%" /p:Configuration=Release /p:Platform=Win64 /m >> "%LOG_FILE%" 2>&1
if %errorlevel% neq 0 goto build_failed

echo Build completed successfully!
echo Log file: %LOG_FILE%
timeout /t 10
exit /b 0

:build_failed
echo [ERROR] Build failed! Error code: %errorlevel% >> "%LOG_FILE%"
echo Build failed! Check log: %LOG_FILE%
pause
exit /b 1