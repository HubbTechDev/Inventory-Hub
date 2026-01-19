"""
Configuration settings for the Inventory Hub scraper.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Scraping settings
USER_AGENT = os.getenv(
    'USER_AGENT',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
)

# Request settings
REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '30'))
MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
RETRY_DELAY = int(os.getenv('RETRY_DELAY', '2'))

# Selenium settings
USE_HEADLESS = os.getenv('USE_HEADLESS', 'True').lower() == 'true'
PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', '30'))

# Output settings
OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'scraped_data')
OUTPUT_FORMAT = os.getenv('OUTPUT_FORMAT', 'json')  # json or csv

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
