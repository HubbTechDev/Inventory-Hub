#!/bin/bash
# Start the Inventory Hub Backend API server

cd "$(dirname "$0")"

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment not found. Please run ./setup.sh first."
    exit 1
fi

# Start the server
echo "Starting Inventory Hub API Server..."
python app.py
