#!/usr/bin/env python3
"""
Initialize the database for Inventory Hub.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import app
from backend.models import db

def init_db():
    """Initialize the database."""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database tables created successfully!")
        
        # Show created tables
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"\n✓ Created tables: {', '.join(tables)}")

if __name__ == '__main__':
    init_db()
