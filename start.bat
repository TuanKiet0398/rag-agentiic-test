@echo off
echo 🚀 Starting Agentic RAG System
echo ================================

REM Check if we're in the right directory
if not exist "agent" (
    echo ❌ Please run this from the agentic project root directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo 📁 Project directory: %CD%

REM Run the startup check
echo 🧪 Running system check...
python start.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo ❌ System check failed. Please fix the issues above.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo 🎯 System check complete!
echo.

REM Ask user what to start
echo What would you like to do?
echo.
echo 1. Start Backend Only
echo 2. Start Frontend Only  
echo 3. Start Both (Recommended)
echo 4. Just run system check (already done)
echo.
set /p choice="Enter choice (1-4): "

if "%choice%"=="1" goto start_backend
if "%choice%"=="2" goto start_frontend
if "%choice%"=="3" goto start_both
if "%choice%"=="4" goto end
echo Invalid choice. Starting both...

:start_both
echo.
echo 🔧 Starting both backend and frontend...
echo.

REM Start backend in new window
echo 🚀 Starting backend server...
start "Agentic RAG Backend" cmd /k "cd agent && python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload"

REM Wait a moment
timeout /t 3 /nobreak >nul

REM Start frontend in new window  
echo 🎨 Starting frontend server...
start "Agentic RAG Frontend" cmd /k "cd src && npm run dev"

echo.
echo ✅ Both servers starting in separate windows!
echo.
echo 📱 Access points:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:8000/docs
echo    LightRAG: http://localhost:9621
echo.
goto end

:start_backend
echo 🚀 Starting backend server...
cd agent
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
goto end

:start_frontend
echo 🎨 Starting frontend server...
cd src
npm run dev
goto end

:end
echo.
echo 👋 Thanks for using Agentic RAG!
pause