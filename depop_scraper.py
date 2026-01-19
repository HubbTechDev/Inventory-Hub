"""
Depop scraper - scrapes inventory listings from Depop marketplace.
Depop is a popular fashion resale marketplace app/website.
"""

import re
import time
from typing import List, Optional
from bs4 import BeautifulSoup
import logging

from scraper import BaseScraper
from models import InventoryItem, InventoryCollection

logger = logging.getLogger(__name__)


class DepopScraper(BaseScraper):
    """
    Scraper for Depop marketplace listings.
    Depop uses JavaScript rendering, so Selenium is recommended.
    """
    
    def __init__(self):
        """Initialize Depop scraper."""
        super().__init__(merchant_name="Depop")
        self.base_url = "https://www.depop.com"
    
    def _extract_price_from_text(self, price_text: str) -> Optional[float]:
        """Extract price from Depop price text."""
        if not price_text:
            return None
        
        # Handle various currency formats (£, $, €)
        price_match = re.search(r'[£$€]?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)', price_text.replace(',', ''))
        if price_match:
            try:
                return float(price_match.group(1))
            except ValueError:
                return None
        return None
    
    def _detect_currency(self, price_text: str) -> str:
        """Detect currency from price text."""
        if not price_text:
            return "USD"
        
        if '£' in price_text:
            return "GBP"
        elif '€' in price_text:
            return "EUR"
        elif '$' in price_text:
            return "USD"
        
        return "USD"  # Default to USD
    
    def _extract_size(self, size_text: str) -> Optional[str]:
        """Extract size information."""
        if not size_text:
            return None
        
        size_text = size_text.strip()
        # Common size patterns
        if re.search(r'\b(XS|S|M|L|XL|XXL)\b', size_text, re.IGNORECASE):
            return size_text
        if re.search(r'\b\d+\b', size_text):  # Numeric sizes
            return size_text
        
        return size_text if size_text else None
    
    def scrape_listing(self, url: str) -> List[InventoryItem]:
        """
        Scrape a single Depop product listing.
        
        Args:
            url: URL of the Depop product listing
            
        Returns:
            List containing single InventoryItem
        """
        logger.info(f"Scraping Depop listing: {url}")
        
        try:
            # Depop requires Selenium for JavaScript rendering
            html = self._get_html(url, use_selenium=True)
            soup = self._parse_html(html)
            
            # Extract title
            title_elem = soup.select_one('h1[data-testid="product__title"], h1.product-title, h1')
            title = title_elem.get_text(strip=True) if title_elem else "Unknown Product"
            
            # Extract price
            price_elem = soup.select_one('p[data-testid="product__price"], span.price, p.product-price')
            price_text = price_elem.get_text(strip=True) if price_elem else ""
            price = self._extract_price_from_text(price_text)
            currency = self._detect_currency(price_text)
            
            # Extract description
            desc_elem = soup.select_one('p[data-testid="product__description"], div.product-description, div.description')
            description = desc_elem.get_text(strip=True) if desc_elem else None
            
            # Extract brand
            brand_elem = soup.select_one('a[data-testid="product__brand"], span.brand, a.product-brand')
            brand = brand_elem.get_text(strip=True) if brand_elem else None
            
            # Extract category
            category_elem = soup.select_one('a[data-testid="product__category"], span.category, nav.breadcrumb')
            category = category_elem.get_text(strip=True) if category_elem else None
            
            # Extract size information
            size_elem = soup.select_one('p[data-testid="product__size"], span.size, div.product-size')
            size = self._extract_size(size_elem.get_text(strip=True) if size_elem else "")
            
            # Extract condition (Depop items are typically used/vintage)
            condition_elem = soup.select_one('p[data-testid="product__condition"], span.condition')
            condition_text = condition_elem.get_text(strip=True) if condition_elem else ""
            
            # Normalize condition
            if "new" in condition_text.lower():
                condition = "new"
            elif "like new" in condition_text.lower() or "excellent" in condition_text.lower():
                condition = "like new"
            else:
                condition = "used"  # Most Depop items are used/vintage
            
            # Extract image
            image_elem = soup.select_one('img[data-testid="product__image"], img.product-image, picture img')
            image_url = image_elem.get('src') if image_elem else None
            if image_url and not image_url.startswith('http'):
                image_url = self.base_url + image_url
            
            # Check if sold
            sold_elem = soup.select_one('[data-testid="product__sold"], .sold-badge, span.sold')
            in_stock = sold_elem is None
            
            # Extract product ID from URL
            sku_match = re.search(r'/products/([a-zA-Z0-9\-_]+)', url)
            sku = f"DEPOP-{sku_match.group(1)}" if sku_match else None
            
            # Store size in custom_fields
            custom_fields = {}
            if size:
                custom_fields['size'] = size
            
            item = InventoryItem(
                title=title,
                price=price,
                currency=currency,
                sku=sku,
                description=description,
                brand=brand,
                category=category,
                image_url=image_url,
                product_url=url,
                merchant=self.merchant_name,
                condition=condition,
                in_stock=in_stock,
                custom_fields=custom_fields if custom_fields else None
            )
            
            logger.info(f"Successfully scraped Depop item: {title}")
            return [item]
            
        except Exception as e:
            logger.error(f"Error scraping Depop listing {url}: {e}")
            return []
    
    def scrape_multiple_pages(self, start_url: str, max_pages: int = 5) -> InventoryCollection:
        """
        Scrape multiple pages of Depop listings.
        
        Args:
            start_url: Starting URL (search results, category, or shop page)
            max_pages: Maximum number of pages to scrape
            
        Returns:
            InventoryCollection with all scraped items
        """
        logger.info(f"Starting multi-page Depop scrape from {start_url}")
        collection = InventoryCollection()
        
        for page_num in range(1, max_pages + 1):
            # Depop uses offset-based pagination
            offset = (page_num - 1) * 20  # Assuming 20 items per page
            
            if '?' in start_url:
                page_url = f"{start_url}&offset={offset}"
            else:
                page_url = f"{start_url}?offset={offset}"
            
            logger.info(f"Scraping Depop page {page_num}/{max_pages}: {page_url}")
            
            try:
                html = self._get_html(page_url, use_selenium=True)
                soup = self._parse_html(html)
                
                # Find product links (Depop-specific selectors)
                product_links = soup.select('a[href*="/products/"], a[data-testid="product-card"]')
                
                if not product_links:
                    logger.warning(f"No product links found on Depop page {page_num}")
                    break
                
                # Extract unique URLs
                urls_seen = set()
                for link in product_links:
                    product_url = link.get('href')
                    if product_url:
                        if not product_url.startswith('http'):
                            product_url = self.base_url + product_url
                        
                        # Avoid duplicates
                        if product_url in urls_seen:
                            continue
                        urls_seen.add(product_url)
                        
                        items = self.scrape_listing(product_url)
                        collection.add_items(items)
                        
                        # Add delay to avoid overwhelming the server
                        time.sleep(2)
                
                # Check if we've reached the last page
                if len(product_links) == 0:
                    logger.info("No more products found, stopping pagination")
                    break
                
            except Exception as e:
                logger.error(f"Error scraping Depop page {page_num}: {e}")
                break
        
        logger.info(f"Completed Depop scraping. Total items: {len(collection)}")
        return collection
