"""
Base scraper class for inventory data extraction.
"""

import logging
import time
from abc import ABC, abstractmethod
from typing import List, Optional
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from models import InventoryItem, InventoryCollection
from config import (
    USER_AGENT, REQUEST_TIMEOUT, MAX_RETRIES, RETRY_DELAY,
    USE_HEADLESS, PAGE_LOAD_TIMEOUT, LOG_LEVEL
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Abstract base class for inventory scrapers."""
    
    def __init__(self, merchant_name: str):
        """
        Initialize the base scraper.
        
        Args:
            merchant_name: Name of the merchant/platform being scraped
        """
        self.merchant_name = merchant_name
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
        self.inventory = InventoryCollection()
        self.driver: Optional[webdriver.Chrome] = None
    
    def _get_html(self, url: str, use_selenium: bool = False) -> str:
        """
        Fetch HTML content from a URL.
        
        Args:
            url: The URL to fetch
            use_selenium: Whether to use Selenium for JavaScript-rendered content
            
        Returns:
            HTML content as string
        """
        if use_selenium:
            return self._get_html_selenium(url)
        else:
            return self._get_html_requests(url)
    
    def _get_html_requests(self, url: str) -> str:
        """Fetch HTML using requests library with retry logic."""
        for attempt in range(MAX_RETRIES):
            try:
                logger.info(f"Fetching {url} (attempt {attempt + 1}/{MAX_RETRIES})")
                response = self.session.get(url, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                logger.warning(f"Request failed: {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                else:
                    logger.error(f"Failed to fetch {url} after {MAX_RETRIES} attempts")
                    raise
    
    def _get_html_selenium(self, url: str) -> str:
        """Fetch HTML using Selenium for JavaScript-rendered content."""
        if self.driver is None:
            self._initialize_selenium()
        
        try:
            logger.info(f"Fetching {url} with Selenium")
            self.driver.get(url)
            time.sleep(2)  # Wait for dynamic content to load
            return self.driver.page_source
        except Exception as e:
            logger.error(f"Selenium fetch failed: {e}")
            raise
    
    def _initialize_selenium(self):
        """Initialize Selenium WebDriver."""
        logger.info("Initializing Selenium WebDriver")
        chrome_options = Options()
        
        if USE_HEADLESS:
            chrome_options.add_argument('--headless')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(f'user-agent={USER_AGENT}')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    
    def _parse_html(self, html: str) -> BeautifulSoup:
        """
        Parse HTML content with BeautifulSoup.
        
        Args:
            html: HTML content string
            
        Returns:
            BeautifulSoup object
        """
        return BeautifulSoup(html, 'lxml')
    
    @abstractmethod
    def scrape_listing(self, url: str) -> List[InventoryItem]:
        """
        Scrape a single listing page.
        
        Args:
            url: URL of the listing page
            
        Returns:
            List of InventoryItem objects
        """
        pass
    
    @abstractmethod
    def scrape_multiple_pages(self, start_url: str, max_pages: int = 5) -> InventoryCollection:
        """
        Scrape multiple pages of listings.
        
        Args:
            start_url: Starting URL for pagination
            max_pages: Maximum number of pages to scrape
            
        Returns:
            InventoryCollection with all scraped items
        """
        pass
    
    def cleanup(self):
        """Clean up resources (close Selenium driver, etc.)."""
        if self.driver:
            logger.info("Closing Selenium WebDriver")
            self.driver.quit()
            self.driver = None
        
        if self.session:
            self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
