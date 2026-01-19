#!/bin/bash

echo "🚀 Inventory Hub - Quick Start"
echo "================================"

# Check Python version
echo "📋 Checking Python version..."
python3 --version || { echo "❌ Python 3 not found. Please install Python 3.8+"; exit 1; }

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "✓ .env created from .env.example"
fi

# Initialize database
echo "🗄️  Initializing database..."
python3 -c "from backend.app import app; from backend.models import db; app.app_context().push(); db.create_all(); print('✓ Database ready')"

# Start the server
echo ""
echo "✅ Setup complete!"
echo "🌐 Starting web server..."
echo "📱 Web App: http://localhost:5000"
echo "🔌 API: http://localhost:5000/api/"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================"
echo ""

# Open browser (optional)
sleep 2
if command -v open &> /dev/null; then
    open http://localhost:5000
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:5000
fi

# Run the app
python3 run.py
