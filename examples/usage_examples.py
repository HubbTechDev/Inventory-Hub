"""
Example: Using the scraper programmatically.
"""

import sys
import os

# Add parent directory to path to import project modules
# This is necessary for examples to import from the parent directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generic_scraper import GenericEcommerceScraper
from models import InventoryItem, InventoryCollection


def example_single_product_scrape():
    """Example: Scrape a single product."""
    print("Example 1: Single Product Scrape")
    print("-" * 50)
    
    # Create scraper
    scraper = GenericEcommerceScraper(
        merchant_name="ExampleStore",
        use_selenium=False
    )
    
    # Scrape a product (replace with actual URL)
    product_url = "https://example.com/product/123"
    
    try:
        items = scraper.scrape_listing(product_url)
        
        if items:
            item = items[0]
            print(f"Title: {item.title}")
            print(f"Price: ${item.price}")
            print(f"In Stock: {item.in_stock}")
            print(f"\nFull item data:")
            print(item.to_json())
        else:
            print("No items found")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        scraper.cleanup()


def example_multiple_pages_scrape():
    """Example: Scrape multiple pages."""
    print("\nExample 2: Multi-Page Scrape")
    print("-" * 50)
    
    # Create scraper with custom selectors
    scraper = GenericEcommerceScraper(
        merchant_name="ExampleStore",
        title_selector="h1.product-name",
        price_selector="span.price-value",
        use_selenium=False
    )
    
    # Scrape category page
    category_url = "https://example.com/category/electronics"
    
    try:
        collection = scraper.scrape_multiple_pages(
            category_url,
            max_pages=3
        )
        
        print(f"Total items scraped: {len(collection)}")
        
        # Display first few items
        for i, item in enumerate(collection):
            if i >= 3:  # Show only first 3
                break
            print(f"\nItem {i+1}:")
            print(f"  Title: {item.title}")
            print(f"  Price: ${item.price}")
        
        # Save to file
        collection.save_to_json("example_output.json")
        print("\nSaved to example_output.json")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        scraper.cleanup()


def example_custom_data_processing():
    """Example: Process scraped data."""
    print("\nExample 3: Custom Data Processing")
    print("-" * 50)
    
    # Create some sample items
    collection = InventoryCollection()
    
    items = [
        InventoryItem(
            title="Wireless Mouse",
            price=29.99,
            sku="MOUSE-001",
            in_stock=True,
            merchant="TechStore"
        ),
        InventoryItem(
            title="USB Keyboard",
            price=49.99,
            sku="KEYB-001",
            in_stock=True,
            merchant="TechStore"
        ),
        InventoryItem(
            title="Laptop Stand",
            price=39.99,
            sku="STAND-001",
            in_stock=False,
            merchant="TechStore"
        )
    ]
    
    collection.add_items(items)
    
    # Process data
    in_stock_items = [item for item in collection if item.in_stock]
    total_value = sum(item.price for item in in_stock_items if item.price)
    
    print(f"Total items: {len(collection)}")
    print(f"In stock: {len(in_stock_items)}")
    print(f"Total value of in-stock items: ${total_value:.2f}")
    
    # Save in different formats
    collection.save_to_json("example_inventory.json")
    collection.save_to_csv("example_inventory.csv")
    print("\nSaved to example_inventory.json and example_inventory.csv")


def example_with_context_manager():
    """Example: Using scraper with context manager."""
    print("\nExample 4: Using Context Manager")
    print("-" * 50)
    
    # Using 'with' statement ensures cleanup
    with GenericEcommerceScraper(merchant_name="Example") as scraper:
        # Scraper will be automatically cleaned up
        print("Scraper initialized with context manager")
        print("Resources will be automatically cleaned up when done")


if __name__ == "__main__":
    print("Inventory Hub - Usage Examples")
    print("=" * 50)
    
    # Note: These examples use placeholder URLs
    # Replace with actual URLs to test
    
    print("\nNote: These examples use placeholder URLs.")
    print("Replace with actual URLs in the code to test scraping.\n")
    
    # Uncomment to run examples:
    # example_single_product_scrape()
    # example_multiple_pages_scrape()
    example_custom_data_processing()
    example_with_context_manager()
    
    print("\n" + "=" * 50)
    print("Examples completed!")
