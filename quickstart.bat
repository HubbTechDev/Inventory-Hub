@echo off
echo 🚀 Inventory Hub - Quick Start
echo ================================

REM Check Python
echo 📋 Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install --upgrade pip >nul
pip install -q -r requirements.txt

REM Create .env if it doesn't exist
if not exist ".env" (
    echo ⚙️  Creating .env file...
    copy .env.example .env >nul
    echo ✓ .env created from .env.example
)

REM Initialize database
echo 🗄️  Initializing database...
python -c "from backend.app import app; from backend.models import db; app.app_context().push(); db.create_all(); print('✓ Database ready')"

REM Start the server
echo.
echo ✅ Setup complete!
echo 🌐 Starting web server...
echo 📱 Web App: http://localhost:5000
echo 🔌 API: http://localhost:5000/api/
echo.
echo Press Ctrl+C to stop the server
echo ================================
echo.

REM Open browser
timeout /t 2 /nobreak >nul
start http://localhost:5000

REM Run the app
python run.py
