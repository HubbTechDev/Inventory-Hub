"""
Examples of using Mercari and Depop scrapers.
"""

import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mercari_scraper import MercariScraper
from depop_scraper import DepopScraper
from models import InventoryCollection


def example_mercari_scraper():
    """Example: Scrape Mercari listings."""
    print("Example: Mercari Scraper")
    print("-" * 50)
    
    # Initialize Mercari scraper
    scraper = MercariScraper()
    
    try:
        # Example product URL (replace with actual Mercari URL to test)
        product_url = "https://www.mercari.com/us/item/m12345678/"
        
        print(f"\nScraping Mercari product: {product_url}")
        print("Note: This is an example URL. Replace with a real Mercari URL to test.\n")
        
        # Scrape single item
        # items = scraper.scrape_listing(product_url)
        # if items:
        #     item = items[0]
        #     print(f"Title: {item.title}")
        #     print(f"Price: ${item.price}")
        #     print(f"Condition: {item.condition}")
        #     print(f"In Stock: {item.in_stock}")
        
        # Example: Scrape search results
        search_url = "https://www.mercari.com/search/?keyword=vintage+shirt"
        print(f"To scrape search results, use:")
        print(f"collection = scraper.scrape_multiple_pages('{search_url}', max_pages=3)")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        scraper.cleanup()
        print("\nMercari scraper cleaned up")


def example_depop_scraper():
    """Example: Scrape Depop listings."""
    print("\n\nExample: Depop Scraper")
    print("-" * 50)
    
    # Initialize Depop scraper
    scraper = DepopScraper()
    
    try:
        # Example product URL (replace with actual Depop URL to test)
        product_url = "https://www.depop.com/products/username-product-id/"
        
        print(f"\nScraping Depop product: {product_url}")
        print("Note: This is an example URL. Replace with a real Depop URL to test.\n")
        
        # Scrape single item
        # items = scraper.scrape_listing(product_url)
        # if items:
        #     item = items[0]
        #     print(f"Title: {item.title}")
        #     print(f"Price: {item.currency} {item.price}")
        #     print(f"Condition: {item.condition}")
        #     print(f"Brand: {item.brand}")
        #     if item.custom_fields and 'size' in item.custom_fields:
        #         print(f"Size: {item.custom_fields['size']}")
        
        # Example: Scrape shop listings
        shop_url = "https://www.depop.com/username/"
        print(f"To scrape a shop, use:")
        print(f"collection = scraper.scrape_multiple_pages('{shop_url}', max_pages=5)")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        scraper.cleanup()
        print("\nDepop scraper cleaned up")


def example_save_multiple_merchants():
    """Example: Scrape from multiple merchants and combine results."""
    print("\n\nExample: Multi-Merchant Scraping")
    print("-" * 50)
    
    combined_collection = InventoryCollection()
    
    # Mercari items
    print("\n1. Scraping Mercari...")
    mercari_scraper = MercariScraper()
    try:
        # mercari_collection = mercari_scraper.scrape_multiple_pages(
        #     "https://www.mercari.com/search/?keyword=sneakers",
        #     max_pages=2
        # )
        # combined_collection.add_items(mercari_collection.items)
        print("   (Add Mercari items to combined collection)")
    finally:
        mercari_scraper.cleanup()
    
    # Depop items
    print("2. Scraping Depop...")
    depop_scraper = DepopScraper()
    try:
        # depop_collection = depop_scraper.scrape_multiple_pages(
        #     "https://www.depop.com/search/?q=sneakers",
        #     max_pages=2
        # )
        # combined_collection.add_items(depop_collection.items)
        print("   (Add Depop items to combined collection)")
    finally:
        depop_scraper.cleanup()
    
    # Save combined results
    print("\n3. Saving combined results...")
    # combined_collection.save_to_json("all_merchants_inventory.json")
    # combined_collection.save_to_csv("all_merchants_inventory.csv")
    
    print(f"\nTotal items from all merchants: {len(combined_collection)}")
    print("Combined inventory saved!")


def example_filter_and_analyze():
    """Example: Filter and analyze scraped data."""
    print("\n\nExample: Data Analysis")
    print("-" * 50)
    
    # Create sample collection
    collection = InventoryCollection()
    
    from models import InventoryItem
    
    # Add sample Mercari items
    collection.add_items([
        InventoryItem(
            title="Vintage Nike Sneakers",
            price=45.00,
            merchant="Mercari",
            condition="good",
            in_stock=True
        ),
        InventoryItem(
            title="Adidas Running Shoes",
            price=60.00,
            merchant="Mercari",
            condition="like new",
            in_stock=True
        ),
    ])
    
    # Add sample Depop items
    collection.add_items([
        InventoryItem(
            title="Vintage Band T-Shirt",
            price=25.00,
            merchant="Depop",
            condition="used",
            in_stock=True,
            currency="USD"
        ),
        InventoryItem(
            title="Designer Jacket",
            price=120.00,
            merchant="Depop",
            condition="like new",
            in_stock=False,
            currency="USD"
        ),
    ])
    
    # Analyze data
    print(f"\nTotal items: {len(collection)}")
    
    # Filter by merchant
    mercari_items = [item for item in collection if item.merchant == "Mercari"]
    depop_items = [item for item in collection if item.merchant == "Depop"]
    
    print(f"Mercari items: {len(mercari_items)}")
    print(f"Depop items: {len(depop_items)}")
    
    # Filter by stock
    in_stock = [item for item in collection if item.in_stock]
    print(f"In stock items: {len(in_stock)}")
    
    # Calculate average price
    prices = [item.price for item in collection if item.price]
    avg_price = sum(prices) / len(prices) if prices else 0
    print(f"Average price: ${avg_price:.2f}")
    
    # Filter by condition
    like_new = [item for item in collection if item.condition == "like new"]
    print(f"'Like new' items: {len(like_new)}")
    
    # Calculate total inventory value
    total_value = sum(item.price for item in in_stock if item.price)
    print(f"Total value of in-stock items: ${total_value:.2f}")


if __name__ == "__main__":
    print("=" * 50)
    print("Mercari & Depop Scraper Examples")
    print("=" * 50)
    
    print("\nNote: These examples use placeholder URLs.")
    print("Uncomment the scraping code and use real URLs to test.\n")
    
    # Run examples
    example_mercari_scraper()
    example_depop_scraper()
    example_save_multiple_merchants()
    example_filter_and_analyze()
    
    print("\n" + "=" * 50)
    print("Examples completed!")
    print("=" * 50)
