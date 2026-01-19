#!/bin/bash
# Quick start script for Inventory Hub Backend API

echo "========================================="
echo "Inventory Hub Backend Setup"
echo "========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Navigate to backend directory
cd "$(dirname "$0")"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Copy .env.example to .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "✓ .env file created"
    echo "⚠️  Please edit .env to configure your settings"
fi

# Run tests
echo ""
echo "Running setup tests..."
python test_setup.py

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================="
    echo "✓ Setup Complete!"
    echo "========================================="
    echo ""
    echo "To start the server:"
    echo "  cd backend"
    echo "  source venv/bin/activate"
    echo "  python app.py"
    echo ""
    echo "Or run: ./start_server.sh"
    echo ""
else
    echo ""
    echo "❌ Setup tests failed. Please check the errors above."
    exit 1
fi
