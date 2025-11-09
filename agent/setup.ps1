# Agentic RAG System - PowerShell Setup Script

Write-Host "🚀 Starting Agentic RAG System Setup..." -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "pyproject.toml")) {
    Write-Host "❌ Error: Please run this script from the agent directory" -ForegroundColor Red
    Write-Host "   Expected location: d:\Workspace\agentic\agent\" -ForegroundColor Yellow
    exit 1
}

Write-Host "📦 Installing dependencies with Poetry..." -ForegroundColor Blue

# Check if Poetry is installed
$poetryInstalled = $false
try {
    poetry --version | Out-Null
    $poetryInstalled = $true
    Write-Host "✅ Poetry found" -ForegroundColor Green
} catch {
    Write-Host "🔧 Installing Poetry..." -ForegroundColor Yellow
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
    $env:PATH = "$env:USERPROFILE\.local\bin;$env:PATH"
}

# Install dependencies
Write-Host "📚 Installing Python dependencies..." -ForegroundColor Blue
poetry install

Write-Host "🔧 Setting up environment..." -ForegroundColor Blue

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "📝 Creating .env file..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "⚠️  Please edit .env file and add your API keys:" -ForegroundColor Yellow
    Write-Host "   - OPENAI_API_KEY=your_openai_key" -ForegroundColor Cyan
    Write-Host "   - TAVILY_API_KEY=your_tavily_key" -ForegroundColor Cyan
    Write-Host "   - LIGHTRAG_URL=http://localhost:9621" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "🎯 Next steps:" -ForegroundColor Blue
Write-Host "1. Edit .env file with your API keys" -ForegroundColor White
Write-Host "2. Make sure LightRAG is running on http://localhost:9621" -ForegroundColor White  
Write-Host "3. Run: poetry run python src/main.py" -ForegroundColor White
Write-Host ""
Write-Host "📚 For more details, see: STARTUP_GUIDE.md" -ForegroundColor Blue