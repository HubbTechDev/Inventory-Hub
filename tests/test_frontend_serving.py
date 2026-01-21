"""
Tests for frontend static file serving.
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.app import create_app


class TestFrontendServing(unittest.TestCase):
    """Test frontend static file serving."""
    
    def setUp(self):
        """Set up test client."""
        self.app = create_app('testing')
        self.client = self.app.test_client()
    
    def test_serve_index_from_root(self):
        """Test that root path serves index.html"""
        response = self.client.get('/')
        
        # Should return HTML content, not JSON
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)
        self.assertIn(b'Inventory Hub', response.data)
    
    def test_serve_static_css(self):
        """Test that CSS files are served correctly"""
        response = self.client.get('/style.css')
        
        self.assertEqual(response.status_code, 200)
        # CSS content type should be text/css
        self.assertIn('text/css', response.content_type)
    
    def test_serve_static_js(self):
        """Test that JavaScript files are served correctly"""
        response = self.client.get('/app.js')
        
        self.assertEqual(response.status_code, 200)
        # JS content type should be application/javascript or text/javascript
        self.assertTrue(
            'javascript' in response.content_type.lower()
        )
    
    def test_spa_routing(self):
        """Test that non-existent paths serve index.html for SPA routing"""
        response = self.client.get('/inventory')
        
        # Should serve index.html for client-side routing
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)
    
    def test_api_routes_not_caught_by_frontend(self):
        """Test that API routes return proper 404 JSON, not HTML"""
        response = self.client.get('/api/nonexistent')
        
        # Should return JSON 404, not HTML
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIn(b'error', response.data)
    
    def test_debug_paths_endpoint(self):
        """Test that debug endpoint shows correct paths"""
        response = self.client.get('/debug/paths')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('frontend_dir', data)
        self.assertIn('exists', data)
        self.assertIn('files', data)
        self.assertIn('index_exists', data)
        
        # Should find index.html
        self.assertTrue(data['index_exists'])
        self.assertTrue(data['exists'])
        self.assertIn('index.html', data['files'])
        self.assertIn('style.css', data['files'])
        self.assertIn('app.js', data['files'])


if __name__ == '__main__':
    unittest.main()
