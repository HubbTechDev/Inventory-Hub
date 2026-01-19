"""
Generic e-commerce scraper for common listing formats.
This serves as an example implementation that can be customized for specific merchants.
"""

import re
from typing import List, Optional
from bs4 import BeautifulSoup

from scraper import BaseScraper
from models import InventoryItem, InventoryCollection
import logging

logger = logging.getLogger(__name__)


class GenericEcommerceScraper(BaseScraper):
    """
    Generic scraper for common e-commerce listing formats.
    Can be customized via CSS selectors for different platforms.
    """
    
    def __init__(
        self,
        merchant_name: str = "Generic",
        title_selector: str = "h1, .product-title, .item-title",
        price_selector: str = ".price, .product-price, [itemprop='price']",
        description_selector: str = ".description, .product-description, [itemprop='description']",
        image_selector: str = "img.product-image, .main-image img, [itemprop='image']",
        sku_selector: str = ".sku, .product-code, [itemprop='sku']",
        stock_selector: str = ".stock, .availability, [itemprop='availability']",
        use_selenium: bool = False
    ):
        """
        Initialize the generic scraper with customizable selectors.
        
        Args:
            merchant_name: Name of the merchant
            title_selector: CSS selector for product title
            price_selector: CSS selector for price
            description_selector: CSS selector for description
            image_selector: CSS selector for product image
            sku_selector: CSS selector for SKU
            stock_selector: CSS selector for stock status
            use_selenium: Whether to use Selenium for scraping
        """
        super().__init__(merchant_name)
        self.title_selector = title_selector
        self.price_selector = price_selector
        self.description_selector = description_selector
        self.image_selector = image_selector
        self.sku_selector = sku_selector
        self.stock_selector = stock_selector
        self.use_selenium = use_selenium
    
    def _extract_price(self, price_text: str) -> Optional[float]:
        """
        Extract numeric price from text.
        
        Args:
            price_text: Text containing price
            
        Returns:
            Float price or None
        """
        if not price_text:
            return None
        
        # Remove currency symbols and commas, then extract numbers
        cleaned_text = price_text.replace(',', '').replace('$', '').replace('£', '').replace('€', '')
        price_match = re.search(r'(\d+(?:\.\d{2})?)', cleaned_text)
        if price_match:
            try:
                return float(price_match.group())
            except ValueError:
                return None
        return None
    
    def _extract_stock_status(self, stock_text: str) -> bool:
        """
        Determine if item is in stock from text.
        
        Args:
            stock_text: Text containing stock information
            
        Returns:
            True if in stock, False otherwise
        """
        if not stock_text:
            return True  # Assume in stock if not specified
        
        stock_text = stock_text.lower()
        out_of_stock_keywords = ['out of stock', 'sold out', 'unavailable', 'not available']
        return not any(keyword in stock_text for keyword in out_of_stock_keywords)
    
    def scrape_listing(self, url: str) -> List[InventoryItem]:
        """
        Scrape a single product listing.
        
        Args:
            url: URL of the product listing
            
        Returns:
            List containing single InventoryItem
        """
        logger.info(f"Scraping listing: {url}")
        
        try:
            html = self._get_html(url, use_selenium=self.use_selenium)
            soup = self._parse_html(html)
            
            # Extract product information
            title_elem = soup.select_one(self.title_selector)
            title = title_elem.get_text(strip=True) if title_elem else "Unknown"
            
            price_elem = soup.select_one(self.price_selector)
            price_text = price_elem.get_text(strip=True) if price_elem else ""
            price = self._extract_price(price_text)
            
            desc_elem = soup.select_one(self.description_selector)
            description = desc_elem.get_text(strip=True) if desc_elem else None
            
            img_elem = soup.select_one(self.image_selector)
            image_url = img_elem.get('src') if img_elem else None
            
            sku_elem = soup.select_one(self.sku_selector)
            sku = sku_elem.get_text(strip=True) if sku_elem else None
            
            stock_elem = soup.select_one(self.stock_selector)
            stock_text = stock_elem.get_text(strip=True) if stock_elem else ""
            in_stock = self._extract_stock_status(stock_text)
            
            item = InventoryItem(
                title=title,
                price=price,
                description=description,
                image_url=image_url,
                sku=sku,
                product_url=url,
                merchant=self.merchant_name,
                in_stock=in_stock
            )
            
            logger.info(f"Successfully scraped: {title}")
            return [item]
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return []
    
    def scrape_multiple_pages(self, start_url: str, max_pages: int = 5) -> InventoryCollection:
        """
        Scrape multiple pages of listings.
        
        Args:
            start_url: Starting URL (should be a category or search page)
            max_pages: Maximum number of pages to scrape
            
        Returns:
            InventoryCollection with all scraped items
        """
        logger.info(f"Starting multi-page scrape from {start_url}")
        collection = InventoryCollection()
        
        for page_num in range(1, max_pages + 1):
            # Construct page URL (this is generic, may need customization)
            if '?' in start_url:
                page_url = f"{start_url}&page={page_num}"
            else:
                page_url = f"{start_url}?page={page_num}"
            
            logger.info(f"Scraping page {page_num}/{max_pages}: {page_url}")
            
            try:
                html = self._get_html(page_url, use_selenium=self.use_selenium)
                soup = self._parse_html(html)
                
                # Find product links (generic selectors, may need customization)
                product_links = soup.select('a.product-link, a[href*="/product/"], a[href*="/item/"]')
                
                if not product_links:
                    logger.warning(f"No product links found on page {page_num}")
                    break
                
                for link in product_links[:10]:  # Limit to 10 products per page
                    product_url = link.get('href')
                    if product_url and not product_url.startswith('http'):
                        # Handle relative URLs
                        from urllib.parse import urljoin
                        product_url = urljoin(page_url, product_url)
                    
                    if product_url:
                        items = self.scrape_listing(product_url)
                        collection.add_items(items)
                
            except Exception as e:
                logger.error(f"Error scraping page {page_num}: {e}")
                break
        
        logger.info(f"Completed scraping. Total items: {len(collection)}")
        return collection


class CustomMerchantScraper(GenericEcommerceScraper):
    """
    Example of a customized scraper for a specific merchant.
    Inherit from GenericEcommerceScraper and override selectors.
    """
    
    def __init__(self):
        super().__init__(
            merchant_name="CustomMerchant",
            title_selector="h1.product-name",
            price_selector="span.price-value",
            description_selector="div.product-desc",
            image_selector="img.main-product-image",
            sku_selector="span.product-sku",
            stock_selector="div.stock-info",
            use_selenium=False  # Set to True if JavaScript rendering needed
        )
