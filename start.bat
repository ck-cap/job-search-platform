@echo off
setlocal enabledelayedexpansion

:: Resume Analyzer Platform Startup Script (Windows)
:: This script provides multiple ways to start the frontend and backend together

title Resume Analyzer Platform

:: Colors for output (Windows doesn't support colors in batch as easily, using echo)
set "INFO=[INFO]"
set "SUCCESS=[SUCCESS]"
set "WARNING=[WARNING]"
set "ERROR=[ERROR]"

:: Function to check if a command exists
where /q %1 >nul 2>&1
if %errorlevel% == 0 (
    exit /b 0
) else (
    exit /b 1
)

:: Function to kill processes on specific ports
:cleanup_ports
echo %INFO% Cleaning up processes on ports 3000 and 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000') do (
    echo %WARNING% Killing process on port 3000
    taskkill /F /PID %%a >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    echo %WARNING% Killing process on port 8000
    taskkill /F /PID %%a >nul 2>&1
)
timeout /t 2 >nul
goto :eof

:: Function to start with Docker
:start_docker
echo %INFO% Starting Resume Analyzer Platform with Docker...

where docker >nul 2>&1
if %errorlevel% neq 0 (
    echo %ERROR% Docker is not installed. Please install Docker first.
    exit /b 1
)

where docker-compose >nul 2>&1
if %errorlevel% neq 0 (
    echo %ERROR% Docker Compose is not installed. Please install Docker Compose first.
    exit /b 1
)

call :cleanup_ports

echo %INFO% Building and starting containers...
docker-compose down --remove-orphans >nul 2>&1
docker-compose up --build
goto :eof

:: Function to start locally
:start_local
echo %INFO% Starting Resume Analyzer Platform locally...

:: Check prerequisites
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo %ERROR% Python is not installed. Please install Python 3.8+ first.
    exit /b 1
)

where node >nul 2>&1
if %errorlevel% neq 0 (
    echo %ERROR% Node.js is not installed. Please install Node.js 18+ first.
    exit /b 1
)

where pnpm >nul 2>&1
if %errorlevel% neq 0 (
    echo %WARNING% pnpm is not installed. Installing pnpm...
    npm install -g pnpm
)

call :cleanup_ports

:: Setup backend
echo %INFO% Setting up backend...
cd job-search-be

if not exist "venv" (
    echo %INFO% Creating Python virtual environment...
    python -m venv venv
)

echo %INFO% Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt

echo %INFO% Starting backend server...
start "Backend" cmd /c "venv\Scripts\activate.bat && uvicorn main:app --reload --port 8000"
cd ..

:: Setup frontend
echo %INFO% Setting up frontend...
cd job-search-fe

if not exist "node_modules" (
    echo %INFO% Installing frontend dependencies...
    pnpm install
)

echo %INFO% Starting frontend server...
start "Frontend" cmd /c "pnpm dev"
cd ..

:: Wait for services to start
echo %INFO% Waiting for services to start...
timeout /t 10 >nul

echo %SUCCESS% Services should be starting...
echo %SUCCESS% Backend API: http://localhost:8000
echo %SUCCESS% Frontend App: http://localhost:3000
echo %INFO% Check the opened terminal windows for logs
echo %INFO% Press any key to continue or Ctrl+C to exit
pause >nul
goto :eof

:: Function to show help
:show_help
echo Resume Analyzer Platform Startup Script (Windows)
echo.
echo Usage: %~nx0 [option]
echo.
echo Options:
echo   docker    Start with Docker (recommended for production)
echo   local     Start locally (recommended for development)
echo   dev       Alias for local
echo   help      Show this help message
echo.
echo Examples:
echo   %~nx0 docker    # Start with Docker
echo   %~nx0 local     # Start locally
echo   %~nx0           # Interactive mode (will ask for preference)
echo.
echo Services:
echo   Backend:  http://localhost:8000 (FastAPI)
echo   Frontend: http://localhost:3000 (Nuxt.js)
goto :eof

:: Main script logic
:main
echo.
echo 🚀 Resume Analyzer Platform Startup Script
echo ===========================================
echo.

if "%~1"=="docker" (
    call :start_docker
) else if "%~1"=="local" (
    call :start_local
) else if "%~1"=="dev" (
    call :start_local
) else if "%~1"=="help" (
    call :show_help
) else if "%~1"=="-h" (
    call :show_help
) else if "%~1"=="--help" (
    call :show_help
) else if "%~1"=="" (
    echo How would you like to start the platform?
    echo.
    echo 1) Docker (recommended for quick start)
    echo 2) Local development (recommended for coding)
    echo.
    set /p choice="Enter your choice (1 or 2): "
    
    if "!choice!"=="1" (
        call :start_docker
    ) else if "!choice!"=="2" (
        call :start_local
    ) else (
        echo %ERROR% Invalid choice. Please run '%~nx0 help' for usage information.
        exit /b 1
    )
) else (
    echo %ERROR% Unknown option: %~1
    call :show_help
    exit /b 1
)

goto :eof

:: Run main function
call :main %* 