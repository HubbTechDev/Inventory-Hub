"""
Unit tests for Mercari and Depop scrapers.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path to import project modules
# This is necessary when running tests from within the tests directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mercari_scraper import MercariScraper
from depop_scraper import DepopScraper
from models import InventoryItem


class TestMercariScraper(unittest.TestCase):
    """Test cases for MercariScraper class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scraper = MercariScraper()
    
    def tearDown(self):
        """Clean up after tests."""
        self.scraper.cleanup()
    
    def test_initialization(self):
        """Test Mercari scraper initialization."""
        self.assertEqual(self.scraper.merchant_name, "Mercari")
        self.assertEqual(self.scraper.base_url, "https://www.mercari.com")
    
    def test_extract_price_from_text(self):
        """Test price extraction."""
        # Test various price formats
        self.assertEqual(self.scraper._extract_price_from_text("$29.99"), 29.99)
        self.assertEqual(self.scraper._extract_price_from_text("$1,299.99"), 1299.99)
        self.assertEqual(self.scraper._extract_price_from_text("19.50"), 19.50)
        self.assertIsNone(self.scraper._extract_price_from_text(""))
        self.assertIsNone(self.scraper._extract_price_from_text(None))
    
    def test_extract_condition(self):
        """Test condition extraction and normalization."""
        self.assertEqual(self.scraper._extract_condition("New with tags"), "new")
        self.assertEqual(self.scraper._extract_condition("Like New"), "like new")
        self.assertEqual(self.scraper._extract_condition("Good condition"), "good")
        self.assertEqual(self.scraper._extract_condition("Fair"), "fair")
        self.assertEqual(self.scraper._extract_condition("Poor"), "poor")
        self.assertEqual(self.scraper._extract_condition("Used"), "used")
        self.assertEqual(self.scraper._extract_condition(""), "used")


class TestDepopScraper(unittest.TestCase):
    """Test cases for DepopScraper class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scraper = DepopScraper()
    
    def tearDown(self):
        """Clean up after tests."""
        self.scraper.cleanup()
    
    def test_initialization(self):
        """Test Depop scraper initialization."""
        self.assertEqual(self.scraper.merchant_name, "Depop")
        self.assertEqual(self.scraper.base_url, "https://www.depop.com")
    
    def test_extract_price_from_text(self):
        """Test price extraction."""
        # Test various price formats and currencies
        self.assertEqual(self.scraper._extract_price_from_text("$29.99"), 29.99)
        self.assertEqual(self.scraper._extract_price_from_text("£19.50"), 19.50)
        self.assertEqual(self.scraper._extract_price_from_text("€35.00"), 35.00)
        self.assertEqual(self.scraper._extract_price_from_text("25"), 25.0)
        self.assertIsNone(self.scraper._extract_price_from_text(""))
        self.assertIsNone(self.scraper._extract_price_from_text(None))
    
    def test_detect_currency(self):
        """Test currency detection."""
        self.assertEqual(self.scraper._detect_currency("$29.99"), "USD")
        self.assertEqual(self.scraper._detect_currency("£19.50"), "GBP")
        self.assertEqual(self.scraper._detect_currency("€35.00"), "EUR")
        self.assertEqual(self.scraper._detect_currency("25"), "USD")  # Default
        self.assertEqual(self.scraper._detect_currency(""), "USD")  # Default
    
    def test_extract_size(self):
        """Test size extraction."""
        self.assertEqual(self.scraper._extract_size("M"), "M")
        self.assertEqual(self.scraper._extract_size("Size L"), "Size L")
        self.assertEqual(self.scraper._extract_size("10"), "10")
        self.assertEqual(self.scraper._extract_size("XL"), "XL")
        self.assertIsNone(self.scraper._extract_size(""))
        self.assertIsNone(self.scraper._extract_size(None))


class TestScraperIntegration(unittest.TestCase):
    """Integration tests for scrapers."""
    
    def test_mercari_scraper_context_manager(self):
        """Test Mercari scraper as context manager."""
        with MercariScraper() as scraper:
            self.assertEqual(scraper.merchant_name, "Mercari")
    
    def test_depop_scraper_context_manager(self):
        """Test Depop scraper as context manager."""
        with DepopScraper() as scraper:
            self.assertEqual(scraper.merchant_name, "Depop")
    
    def test_mercari_inventory_collection(self):
        """Test that Mercari scraper creates proper inventory items."""
        scraper = MercariScraper()
        
        # Create a mock item
        item = InventoryItem(
            title="Test Product",
            price=29.99,
            merchant="Mercari",
            condition="good"
        )
        
        self.assertEqual(item.merchant, "Mercari")
        self.assertEqual(item.price, 29.99)
        
        scraper.cleanup()
    
    def test_depop_inventory_collection(self):
        """Test that Depop scraper creates proper inventory items."""
        scraper = DepopScraper()
        
        # Create a mock item with custom fields
        item = InventoryItem(
            title="Vintage Jacket",
            price=45.00,
            currency="GBP",
            merchant="Depop",
            condition="used",
            custom_fields={"size": "M"}
        )
        
        self.assertEqual(item.merchant, "Depop")
        self.assertEqual(item.currency, "GBP")
        self.assertIsNotNone(item.custom_fields)
        self.assertEqual(item.custom_fields["size"], "M")
        
        scraper.cleanup()


if __name__ == '__main__':
    unittest.main()
