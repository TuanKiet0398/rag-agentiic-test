@echo off
echo 🚀 Setting up Agentic RAG System...

REM Navigate to agent directory
cd agent

echo 📦 Installing Python dependencies...
REM Install Python dependencies using uv (or pip if uv not available)
where uv >nul 2>&1
if %errorlevel% == 0 (
    uv sync
) else (
    echo ⚠️  uv not found, using pip...
    pip install -e .
)

REM Check if .env file exists, create from example if not
if not exist .env (
    echo 📝 Creating .env file from template...
    copy .env.example .env
    echo ⚠️  Please edit .env file with your API keys:
    echo    - OPENAI_API_KEY=your_openai_api_key
    echo    - TAVILY_API_KEY=your_tavily_api_key
)

REM Navigate back and install frontend dependencies
cd ..

echo 🎨 Installing frontend dependencies...
npm install

echo ✅ Setup complete!
echo.
echo 🔧 To run the system:
echo    1. Edit agent\.env with your API keys
echo    2. Run: npm run dev
echo.
echo 📋 Available commands:
echo    npm run dev        - Start both frontend and backend
echo    npm run dev:agent  - Start backend only
echo    npm run dev:ui     - Start frontend only
echo.
echo 🌐 Access points:
echo    Frontend: http://localhost:3000
echo    Backend:  http://localhost:8000
echo    AG-UI:    http://localhost:8000/ui

pause