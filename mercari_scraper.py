"""
Mercari scraper - scrapes inventory listings from Mercari marketplace.
Mercari is a popular resale marketplace app/website.
"""

import re
import time
from typing import List, Optional
from bs4 import BeautifulSoup
import logging

from scraper import BaseScraper
from models import InventoryItem, InventoryCollection

logger = logging.getLogger(__name__)


class MercariScraper(BaseScraper):
    """
    Scraper for Mercari marketplace listings.
    Mercari uses JavaScript rendering, so Selenium is required.
    """
    
    def __init__(self):
        """Initialize Mercari scraper."""
        super().__init__(merchant_name="Mercari")
        self.base_url = "https://www.mercari.com"
    
    def _extract_price_from_text(self, price_text: str) -> Optional[float]:
        """Extract price from Mercari price text."""
        if not price_text:
            return None
        
        # Remove currency symbols and extract numbers
        price_match = re.search(r'\$?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)', price_text.replace(',', ''))
        if price_match:
            try:
                return float(price_match.group(1))
            except ValueError:
                return None
        return None
    
    def _extract_condition(self, condition_text: str) -> str:
        """Extract and normalize condition from text."""
        if not condition_text:
            return "used"
        
        condition_text = condition_text.lower()
        
        if "like new" in condition_text or "like-new" in condition_text:
            return "like new"
        elif "new" in condition_text:
            return "new"
        elif "good" in condition_text:
            return "good"
        elif "fair" in condition_text:
            return "fair"
        elif "poor" in condition_text:
            return "poor"
        
        return "used"
    
    def scrape_listing(self, url: str) -> List[InventoryItem]:
        """
        Scrape a single Mercari product listing.
        
        Args:
            url: URL of the Mercari product listing
            
        Returns:
            List containing single InventoryItem
        """
        logger.info(f"Scraping Mercari listing: {url}")
        
        try:
            # Mercari requires Selenium for JavaScript rendering
            html = self._get_html(url, use_selenium=True)
            soup = self._parse_html(html)
            
            # Extract title
            title_elem = soup.select_one('h1[data-testid="item-name"], h1.item-name, div[data-testid="item-name"]')
            title = title_elem.get_text(strip=True) if title_elem else "Unknown Product"
            
            # Extract price
            price_elem = soup.select_one('div[data-testid="price"], span.price, div.item-price')
            price_text = price_elem.get_text(strip=True) if price_elem else ""
            price = self._extract_price_from_text(price_text)
            
            # Extract description
            desc_elem = soup.select_one('div[data-testid="description"], div.item-description, p.description')
            description = desc_elem.get_text(strip=True) if desc_elem else None
            
            # Extract condition
            condition_elem = soup.select_one('div[data-testid="condition"], span.condition, div.item-condition')
            condition_text = condition_elem.get_text(strip=True) if condition_elem else ""
            condition = self._extract_condition(condition_text)
            
            # Extract image
            image_elem = soup.select_one('img[data-testid="item-photo"], img.item-image, img.product-image')
            image_url = image_elem.get('src') if image_elem else None
            if image_url and not image_url.startswith('http'):
                image_url = self.base_url + image_url
            
            # Extract brand
            brand_elem = soup.select_one('div[data-testid="brand"], span.brand, div.item-brand')
            brand = brand_elem.get_text(strip=True) if brand_elem else None
            
            # Extract category
            category_elem = soup.select_one('div[data-testid="category"], span.category, nav.breadcrumb')
            category = category_elem.get_text(strip=True) if category_elem else None
            
            # Check stock status (if sold)
            sold_elem = soup.select_one('div[data-testid="sold"], span.sold, div.item-sold')
            in_stock = sold_elem is None  # If "sold" element exists, item is not in stock
            
            # Extract item ID from URL
            sku_match = re.search(r'/m(\d+)', url)
            sku = f"MERC-{sku_match.group(1)}" if sku_match else None
            
            item = InventoryItem(
                title=title,
                price=price,
                currency="USD",
                sku=sku,
                description=description,
                brand=brand,
                category=category,
                image_url=image_url,
                product_url=url,
                merchant=self.merchant_name,
                condition=condition,
                in_stock=in_stock
            )
            
            logger.info(f"Successfully scraped Mercari item: {title}")
            return [item]
            
        except Exception as e:
            logger.error(f"Error scraping Mercari listing {url}: {e}")
            return []
    
    def scrape_multiple_pages(self, start_url: str, max_pages: int = 5) -> InventoryCollection:
        """
        Scrape multiple pages of Mercari listings.
        
        Args:
            start_url: Starting URL (search results or category page)
            max_pages: Maximum number of pages to scrape
            
        Returns:
            InventoryCollection with all scraped items
        """
        logger.info(f"Starting multi-page Mercari scrape from {start_url}")
        collection = InventoryCollection()
        
        for page_num in range(1, max_pages + 1):
            # Construct page URL
            if '?' in start_url:
                page_url = f"{start_url}&page={page_num}"
            else:
                page_url = f"{start_url}?page={page_num}"
            
            logger.info(f"Scraping Mercari page {page_num}/{max_pages}: {page_url}")
            
            try:
                html = self._get_html(page_url, use_selenium=True)
                soup = self._parse_html(html)
                
                # Find product links (Mercari-specific selectors)
                product_links = soup.select('a[href*="/item/"], a[data-testid="item-card"]')
                
                if not product_links:
                    logger.warning(f"No product links found on Mercari page {page_num}")
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
                
            except Exception as e:
                logger.error(f"Error scraping Mercari page {page_num}: {e}")
                break
        
        logger.info(f"Completed Mercari scraping. Total items: {len(collection)}")
        return collection
