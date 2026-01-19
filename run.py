#!/usr/bin/env python3
"""
Run the Inventory Hub application.
Serves both the backend API and frontend static files.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import app
from flask import send_from_directory

# Serve frontend static files
@app.route('/')
def serve_frontend():
    return send_from_directory('frontend/public', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    # Check if it's a static file
    if '.' in path:
        return send_from_directory('frontend/public', path)
    # Otherwise serve index.html for client-side routing
    return send_from_directory('frontend/public', 'index.html')

if __name__ == '__main__':
    # Initialize database if needed
    from backend.models import db
    with app.app_context():
        db.create_all()
        print("✓ Database initialized")
    
    # Run the app
    print(f"✓ Starting Inventory Hub on http://localhost:{app.config['PORT']}")
    print(f"✓ Frontend: http://localhost:{app.config['PORT']}/")
    print(f"✓ API: http://localhost:{app.config['PORT']}/api/")
    
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
