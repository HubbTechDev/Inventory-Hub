#!/usr/bin/env python3
"""
Simple test script to validate the backend API setup.
"""

import sys
import os

# NOTE: Import backend modules from parent directory
# For production, consider proper package installation or restructuring
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from backend.app import create_app
from backend.models import db, User, InventoryItem, ScrapingJob


def test_app_creation():
    """Test that the app can be created."""
    print("Testing app creation...")
    app = create_app('development')
    assert app is not None
    print("✓ App created successfully")
    return app


def test_database_setup(app):
    """Test database setup."""
    print("\nTesting database setup...")
    with app.app_context():
        # Drop all tables and recreate
        db.drop_all()
        db.create_all()
        
        # Verify tables exist
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        expected_tables = ['users', 'inventory_items', 'scraping_jobs']
        for table in expected_tables:
            assert table in tables, f"Table {table} not found"
            print(f"✓ Table '{table}' created")
    
    print("✓ Database setup successful")


def test_user_creation(app):
    """Test user creation."""
    print("\nTesting user creation...")
    with app.app_context():
        # Create a test user
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpass123')
        
        db.session.add(user)
        db.session.commit()
        
        # Retrieve user
        retrieved_user = User.query.filter_by(username='testuser').first()
        assert retrieved_user is not None
        assert retrieved_user.email == 'test@example.com'
        assert retrieved_user.check_password('testpass123')
        assert not retrieved_user.check_password('wrongpass')
        
        print(f"✓ User created: {retrieved_user.to_dict()}")


def test_inventory_item_creation(app):
    """Test inventory item creation."""
    print("\nTesting inventory item creation...")
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        
        # Create inventory item
        item = InventoryItem(
            user_id=user.id,
            title='Test Product',
            price=99.99,
            currency='USD',
            quantity=5,
            sku='TEST-001',
            description='Test product description',
            category='Electronics',
            brand='TestBrand',
            condition='new',
            merchant='TestMerchant',
            in_stock=True
        )
        
        db.session.add(item)
        db.session.commit()
        
        # Retrieve item
        retrieved_item = InventoryItem.query.filter_by(sku='TEST-001').first()
        assert retrieved_item is not None
        assert retrieved_item.title == 'Test Product'
        assert retrieved_item.price == 99.99
        
        print(f"✓ Inventory item created: ID={retrieved_item.id}, Title={retrieved_item.title}")


def test_scraping_job_creation(app):
    """Test scraping job creation."""
    print("\nTesting scraping job creation...")
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        
        # Create scraping job
        job = ScrapingJob(
            user_id=user.id,
            merchant='Mercari',
            url='https://www.mercari.com/search/',
            status='completed',
            items_scraped=10
        )
        
        db.session.add(job)
        db.session.commit()
        
        # Retrieve job
        retrieved_job = ScrapingJob.query.filter_by(user_id=user.id).first()
        assert retrieved_job is not None
        assert retrieved_job.merchant == 'Mercari'
        assert retrieved_job.items_scraped == 10
        
        print(f"✓ Scraping job created: ID={retrieved_job.id}, Items={retrieved_job.items_scraped}")


def test_routes(app):
    """Test that routes are registered."""
    print("\nTesting route registration...")
    with app.app_context():
        client = app.test_client()
        
        # Test health endpoint
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
        print("✓ Health endpoint working")
        
        # Test API info endpoint
        response = client.get('/api')
        assert response.status_code == 200
        data = response.get_json()
        assert 'endpoints' in data
        print("✓ API info endpoint working")


def run_all_tests():
    """Run all tests."""
    print("="*60)
    print("Running Backend API Tests")
    print("="*60)
    
    try:
        app = test_app_creation()
        test_database_setup(app)
        test_user_creation(app)
        test_inventory_item_creation(app)
        test_scraping_job_creation(app)
        test_routes(app)
        
        print("\n" + "="*60)
        print("✓ All tests passed!")
        print("="*60)
        return True
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
