"""
Example: Custom scraper for a fictional e-commerce platform.
This demonstrates how to create a platform-specific scraper.
"""

from generic_scraper import GenericEcommerceScraper
from models import InventoryItem
from typing import List
import logging

logger = logging.getLogger(__name__)


class AmazonStyleScraper(GenericEcommerceScraper):
    """
    Example scraper for Amazon-style product pages.
    Note: This is for educational purposes only.
    """
    
    def __init__(self):
        super().__init__(
            merchant_name="AmazonStyle",
            title_selector="span#productTitle, h1.product-title",
            price_selector="span.a-price-whole, .price-value",
            description_selector="div#productDescription, div.product-description",
            image_selector="img#landingImage, img.product-image",
            sku_selector="th:contains('ASIN') + td, .sku-value",
            stock_selector="div#availability span, .availability-message",
            use_selenium=False
        )


class EtsyStyleScraper(GenericEcommerceScraper):
    """
    Example scraper for Etsy-style handmade product pages.
    Note: This is for educational purposes only.
    """
    
    def __init__(self):
        super().__init__(
            merchant_name="EtsyStyle",
            title_selector="h1[data-buy-box-listing-title], h1.listing-title",
            price_selector="p.price, div.price-value",
            description_selector="div.description-text, p.item-description",
            image_selector="img.listing-image, img[data-listing-id]",
            sku_selector=".listing-id, .product-id",
            stock_selector=".inventory-display, .stock-level",
            use_selenium=True  # Etsy may use JavaScript rendering
        )


class ShopifyStyleScraper(GenericEcommerceScraper):
    """
    Example scraper for Shopify-based stores.
    Many small businesses use Shopify with similar HTML structure.
    """
    
    def __init__(self):
        super().__init__(
            merchant_name="ShopifyStyle",
            title_selector="h1.product-title, h1[itemprop='name']",
            price_selector="span.price, span[itemprop='price']",
            description_selector="div.product-description, div[itemprop='description']",
            image_selector="img.product-featured-image, img[itemprop='image']",
            sku_selector="span.sku, span.variant-sku",
            stock_selector="p.product-inventory, span.inventory-quantity",
            use_selenium=False
        )


# Example usage
if __name__ == "__main__":
    # This is just an example - replace with actual URLs
    print("Example scrapers initialized successfully!")
    print("\nAvailable example scrapers:")
    print("1. AmazonStyleScraper - For Amazon-style product pages")
    print("2. EtsyStyleScraper - For Etsy-style handmade items")
    print("3. ShopifyStyleScraper - For Shopify-based stores")
    print("\nTo use: scraper = AmazonStyleScraper()")
