#!/usr/bin/env python3
"""
Quick start script for Inventory Hub web application.
Works on Windows, macOS, and Linux.
"""

import os
import sys
import subprocess
import platform
import webbrowser
from pathlib import Path

def print_header():
    print("🚀 Inventory Hub - Quick Start")
    print("=" * 50)

def check_python():
    print("📋 Checking Python version...")
    version = sys.version_info
    if version < (3, 8):
        print(f"❌ Python {version.major}.{version.minor} found. Python 3.8+ required.")
        sys.exit(1)
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")

def create_venv():
    venv_path = Path("venv")
    if not venv_path.exists():
        print("📦 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✓ Virtual environment created")
    return venv_path

def get_pip_executable(venv_path):
    if platform.system() == "Windows":
        return venv_path / "Scripts" / "pip.exe"
    else:
        return venv_path / "bin" / "pip"

def get_python_executable(venv_path):
    if platform.system() == "Windows":
        return venv_path / "Scripts" / "python.exe"
    else:
        return venv_path / "bin" / "python"

def install_dependencies(pip_executable):
    print("📥 Installing dependencies...")
    subprocess.run([
        str(pip_executable), 
        "install", 
        "-q", 
        "--upgrade", 
        "pip"
    ], check=True)
    subprocess.run([
        str(pip_executable), 
        "install", 
        "-q", 
        "-r", 
        "requirements.txt"
    ], check=True)
    print("✓ Dependencies installed")

def create_env_file():
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if not env_path.exists() and env_example_path.exists():
        print("⚙️  Creating .env file...")
        env_path.write_text(env_example_path.read_text())
        print("✓ .env created from .env.example")

def initialize_database(python_executable):
    print("🗄️  Initializing database...")
    code = "from backend.app import app; from backend.models import db; app.app_context().push(); db.create_all(); print('✓ Database ready')"
    subprocess.run([str(python_executable), "-c", code], check=True)

def open_browser():
    import time
    time.sleep(2)
    print("🌐 Opening browser...")
    webbrowser.open("http://localhost:5000")

def run_app(python_executable):
    print("\n✅ Setup complete!")
    print("🌐 Starting web server...")
    print("📱 Web App: http://localhost:5000")
    print("🔌 API: http://localhost:5000/api/")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    print()
    
    # Open browser in background
    import threading
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run the app
    subprocess.run([str(python_executable), "run.py"])

def main():
    try:
        print_header()
        check_python()
        venv_path = create_venv()
        pip_exe = get_pip_executable(venv_path)
        python_exe = get_python_executable(venv_path)
        install_dependencies(pip_exe)
        create_env_file()
        initialize_database(python_exe)
        run_app(python_exe)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
