# Agentic RAG System Startup Script (PowerShell)
# Run this to start the complete system

Write-Host "🚀 Starting Agentic RAG System" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Check if we're in the right directory
if (-not (Test-Path "agent")) {
    Write-Host "❌ Please run this from the agentic project root directory" -ForegroundColor Red
    Write-Host "Current directory: $(Get-Location)" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "📁 Project directory: $(Get-Location)" -ForegroundColor Green

# Run the startup check
Write-Host "🧪 Running system check..." -ForegroundColor Yellow
try {
    & python start.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "❌ System check failed. Please fix the issues above." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit $LASTEXITCODE
    }
} catch {
    Write-Host "❌ Failed to run system check: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "🎯 System check complete!" -ForegroundColor Green
Write-Host ""

# Ask user what to start
Write-Host "What would you like to do?" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Start Backend Only" -ForegroundColor White
Write-Host "2. Start Frontend Only" -ForegroundColor White
Write-Host "3. Start Both (Recommended)" -ForegroundColor Green
Write-Host "4. Just run system check (already done)" -ForegroundColor Gray
Write-Host ""

do {
    $choice = Read-Host "Enter choice (1-4)"
} while ($choice -notin @('1','2','3','4'))

switch ($choice) {
    '1' {
        Write-Host ""
        Write-Host "🚀 Starting backend server..." -ForegroundColor Yellow
        Set-Location agent
        & python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
    }
    
    '2' {
        Write-Host ""
        Write-Host "🎨 Starting frontend server..." -ForegroundColor Yellow
        Set-Location src
        & npm run dev
    }
    
    '3' {
        Write-Host ""
        Write-Host "🔧 Starting both backend and frontend..." -ForegroundColor Yellow
        Write-Host ""
        
        # Start backend in new PowerShell window
        Write-Host "🚀 Starting backend server..." -ForegroundColor Green
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\agent'; python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload" -WindowStyle Normal
        
        # Wait a moment
        Start-Sleep -Seconds 3
        
        # Start frontend in new PowerShell window
        Write-Host "🎨 Starting frontend server..." -ForegroundColor Green
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\src'; npm run dev" -WindowStyle Normal
        
        Write-Host ""
        Write-Host "✅ Both servers starting in separate windows!" -ForegroundColor Green
        Write-Host ""
        Write-Host "📱 Access points:" -ForegroundColor Cyan
        Write-Host "   Frontend: " -NoNewline; Write-Host "http://localhost:3000" -ForegroundColor Blue
        Write-Host "   Backend API: " -NoNewline; Write-Host "http://localhost:8000/docs" -ForegroundColor Blue  
        Write-Host "   LightRAG: " -NoNewline; Write-Host "http://localhost:9621" -ForegroundColor Blue
        Write-Host ""
    }
    
    '4' {
        Write-Host "✅ System check already completed!" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "👋 Thanks for using Agentic RAG!" -ForegroundColor Cyan
Read-Host "Press Enter to exit"