#!/usr/bin/env python3
"""
Run the Inventory Hub application.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import app
from backend.models import db

if __name__ == '__main__':
    # Initialize database if needed
    with app.app_context():
        db.create_all()
        print("✓ Database initialized")
    
    # Get config
    host = app.config.get('HOST', '0.0.0.0')
    port = app.config.get('PORT', 5000)
    debug = app.config.get('DEBUG', False)
    
    # Run the app
    print(f"\n✅ Inventory Hub is starting!")
    print(f"🌐 Web App: http://localhost:{port}/")
    print(f"🔌 API: http://localhost:{port}/api/")
    print(f"\n📋 Press Ctrl+C to stop\n")
    
    app.run(
        host=host,
        port=port,
        debug=debug
    )
