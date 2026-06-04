# Kisan Price Intelligence - Setup Script for Windows
# Run this in PowerShell

Write-Host "🌾 Kisan Price Intelligence - Setup" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonVersion = python --version
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check pip
Write-Host "Checking pip..." -ForegroundColor Yellow
if (Get-Command pip -ErrorAction SilentlyContinue) {
    $pipVersion = pip --version
    Write-Host "✅ pip found" -ForegroundColor Green
} else {
    Write-Host "❌ pip not found" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "⚠️  venv already exists, skipping..." -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "✅ Virtual environment activated" -ForegroundColor Green

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip
Write-Host "✅ pip upgraded" -ForegroundColor Green

# Install backend requirements
Write-Host ""
Write-Host "Installing backend dependencies..." -ForegroundColor Yellow
Set-Location backend
pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Backend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Check Firebase config
Write-Host ""
Write-Host "Checking Firebase configuration..." -ForegroundColor Yellow
$firebaseConfig = "..\firebase\firebase-config.json"
if (Test-Path $firebaseConfig) {
    Write-Host "✅ Firebase config found" -ForegroundColor Green
} else {
    Write-Host "⚠️  Firebase config not found" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please follow these steps:" -ForegroundColor Cyan
    Write-Host "1. Go to https://console.firebase.google.com" -ForegroundColor White
    Write-Host "2. Select your project" -ForegroundColor White
    Write-Host "3. Settings → Service Accounts → Generate New Private Key" -ForegroundColor White
    Write-Host "4. Save as: firebase\firebase-config.json" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter after you've downloaded the file..."
    
    if (Test-Path $firebaseConfig) {
        Write-Host "✅ Firebase config found" -ForegroundColor Green
    } else {
        Write-Host "❌ Config file still not found" -ForegroundColor Red
        exit 1
    }
}

# Create .env file
Write-Host ""
Write-Host "Creating .env file..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "⚠️  .env already exists, skipping..." -ForegroundColor Yellow
} else {
    @"
# Firebase Configuration
FIREBASE_CREDENTIALS_PATH=firebase/firebase-config.json

# API Keys
AGMARKNET_API_KEY=
DATA_GOV_API_KEY=

# Telegram Bot
TELEGRAM_BOT_TOKEN=

# App Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production

# Server
PORT=5000
HOST=0.0.0.0
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "✅ .env file created" -ForegroundColor Green
}

# Test Firebase connection
Write-Host ""
Write-Host "Testing Firebase connection..." -ForegroundColor Yellow
python test_firebase.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Firebase connection successful" -ForegroundColor Green
} else {
    Write-Host "⚠️  Firebase test failed (this is normal if Firestore is not enabled)" -ForegroundColor Yellow
}

# Back to root
Set-Location ..

# Summary
Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "🎉 Setup Complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Activate venv: .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "2. Start backend: cd backend; python app.py" -ForegroundColor White
Write-Host "3. Visit: http://localhost:5000" -ForegroundColor White
Write-Host ""
Write-Host "For Telegram bot:" -ForegroundColor Cyan
Write-Host "1. Get token from @BotFather" -ForegroundColor White
Write-Host "2. Update .env with TELEGRAM_BOT_TOKEN" -ForegroundColor White
Write-Host "3. Run: cd telegram_bot; python bot.py" -ForegroundColor White
Write-Host ""