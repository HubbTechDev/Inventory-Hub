"""
Unit tests for the models module.
"""

import unittest
import json
from datetime import datetime
from models import InventoryItem, InventoryCollection


class TestInventoryItem(unittest.TestCase):
    """Test cases for InventoryItem class."""
    
    def test_create_basic_item(self):
        """Test creating a basic inventory item."""
        item = InventoryItem(
            title="Test Product",
            price=29.99,
            sku="TEST-001"
        )
        
        self.assertEqual(item.title, "Test Product")
        self.assertEqual(item.price, 29.99)
        self.assertEqual(item.sku, "TEST-001")
        self.assertEqual(item.currency, "USD")
        self.assertTrue(item.in_stock)
        self.assertIsNotNone(item.scraped_at)
    
    def test_item_with_all_fields(self):
        """Test creating an item with all fields."""
        item = InventoryItem(
            title="Complete Product",
            price=99.99,
            currency="EUR",
            quantity=10,
            sku="PROD-123",
            description="A complete product",
            category="Electronics",
            brand="TestBrand",
            image_url="https://example.com/image.jpg",
            product_url="https://example.com/product/123",
            merchant="TestMerchant",
            condition="new",
            in_stock=True
        )
        
        self.assertEqual(item.title, "Complete Product")
        self.assertEqual(item.price, 99.99)
        self.assertEqual(item.currency, "EUR")
        self.assertEqual(item.quantity, 10)
    
    def test_to_dict(self):
        """Test converting item to dictionary."""
        item = InventoryItem(title="Test", price=10.00)
        item_dict = item.to_dict()
        
        self.assertIsInstance(item_dict, dict)
        self.assertEqual(item_dict['title'], "Test")
        self.assertEqual(item_dict['price'], 10.00)
    
    def test_to_json(self):
        """Test converting item to JSON string."""
        item = InventoryItem(title="Test", price=10.00)
        item_json = item.to_json()
        
        self.assertIsInstance(item_json, str)
        parsed = json.loads(item_json)
        self.assertEqual(parsed['title'], "Test")
    
    def test_from_dict(self):
        """Test creating item from dictionary."""
        data = {
            'title': 'Dict Product',
            'price': 19.99,
            'sku': 'DICT-001',
            'currency': 'USD',
            'in_stock': True,
            'condition': 'new'
        }
        
        item = InventoryItem.from_dict(data)
        self.assertEqual(item.title, 'Dict Product')
        self.assertEqual(item.price, 19.99)


class TestInventoryCollection(unittest.TestCase):
    """Test cases for InventoryCollection class."""
    
    def test_create_empty_collection(self):
        """Test creating an empty collection."""
        collection = InventoryCollection()
        self.assertEqual(len(collection), 0)
    
    def test_add_single_item(self):
        """Test adding a single item."""
        collection = InventoryCollection()
        item = InventoryItem(title="Test", price=10.00)
        
        collection.add_item(item)
        self.assertEqual(len(collection), 1)
    
    def test_add_multiple_items(self):
        """Test adding multiple items at once."""
        collection = InventoryCollection()
        items = [
            InventoryItem(title="Item 1", price=10.00),
            InventoryItem(title="Item 2", price=20.00),
            InventoryItem(title="Item 3", price=30.00)
        ]
        
        collection.add_items(items)
        self.assertEqual(len(collection), 3)
    
    def test_to_dict_list(self):
        """Test converting collection to list of dicts."""
        collection = InventoryCollection()
        collection.add_item(InventoryItem(title="Test 1", price=10.00))
        collection.add_item(InventoryItem(title="Test 2", price=20.00))
        
        dict_list = collection.to_dict_list()
        self.assertIsInstance(dict_list, list)
        self.assertEqual(len(dict_list), 2)
        self.assertEqual(dict_list[0]['title'], 'Test 1')
        self.assertEqual(dict_list[1]['title'], 'Test 2')
    
    def test_to_json(self):
        """Test converting collection to JSON."""
        collection = InventoryCollection()
        collection.add_item(InventoryItem(title="Test", price=10.00))
        
        json_str = collection.to_json()
        self.assertIsInstance(json_str, str)
        parsed = json.loads(json_str)
        self.assertIsInstance(parsed, list)
        self.assertEqual(len(parsed), 1)
    
    def test_iteration(self):
        """Test iterating over collection."""
        collection = InventoryCollection()
        items = [
            InventoryItem(title="Item 1", price=10.00),
            InventoryItem(title="Item 2", price=20.00)
        ]
        collection.add_items(items)
        
        count = 0
        for item in collection:
            count += 1
            self.assertIsInstance(item, InventoryItem)
        
        self.assertEqual(count, 2)


if __name__ == '__main__':
    unittest.main()
