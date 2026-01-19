"""
Integration tests for API endpoints.
"""

import unittest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.app import create_app
from backend.models import db


class TestAuthAPI(unittest.TestCase):
    """Test authentication endpoints."""
    
    def setUp(self):
        """Set up test client and database."""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Clean up database."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_register_user(self):
        """Test user registration."""
        response = self.client.post('/api/auth/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('access_token', data)
        self.assertIn('user', data)
        self.assertEqual(data['user']['username'], 'testuser')
    
    def test_register_duplicate_username(self):
        """Test registration with duplicate username."""
        # Register first user
        self.client.post('/api/auth/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test1@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        # Try to register with same username
        response = self.client.post('/api/auth/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test2@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_login(self):
        """Test user login."""
        # Register user first
        self.client.post('/api/auth/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        # Login
        response = self.client.post('/api/auth/login',
            data=json.dumps({
                'username': 'testuser',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data)
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        response = self.client.post('/api/auth/login',
            data=json.dumps({
                'username': 'nonexistent',
                'password': 'wrongpassword'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 401)


class TestInventoryAPI(unittest.TestCase):
    """Test inventory endpoints."""
    
    def setUp(self):
        """Set up test client and database."""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
        
        # Register and login to get token
        response = self.client.post('/api/auth/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.token = data['access_token']
        self.headers = {'Authorization': f'Bearer {self.token}'}
    
    def tearDown(self):
        """Clean up database."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_list_empty_inventory(self):
        """Test listing inventory when empty."""
        response = self.client.get('/api/inventory', headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['total'], 0)
        self.assertEqual(len(data['items']), 0)
    
    def test_get_statistics(self):
        """Test getting dashboard statistics."""
        response = self.client.get('/api/stats', headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('total_items', data)
        self.assertIn('total_value', data)
        self.assertEqual(data['total_items'], 0)


class TestScrapingAPI(unittest.TestCase):
    """Test scraping endpoints."""
    
    def setUp(self):
        """Set up test client and database."""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
        
        # Register and login to get token
        response = self.client.post('/api/auth/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.token = data['access_token']
        self.headers = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
    
    def tearDown(self):
        """Clean up database."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_list_empty_scraping_jobs(self):
        """Test listing scraping jobs when empty."""
        response = self.client.get('/api/scraping/jobs', headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['total'], 0)


if __name__ == '__main__':
    unittest.main()
