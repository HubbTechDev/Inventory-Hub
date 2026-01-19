"""
Main entry point for the Inventory Hub scraper.
"""

import argparse
import logging
import os
from pathlib import Path
from datetime import datetime

from generic_scraper import GenericEcommerceScraper, CustomMerchantScraper
from mercari_scraper import MercariScraper
from depop_scraper import DepopScraper
from models import InventoryCollection
from config import OUTPUT_DIR, OUTPUT_FORMAT

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for the scraper application."""
    parser = argparse.ArgumentParser(
        description='Inventory Hub - Scrape inventory data from merchant listings'
    )
    parser.add_argument(
        'url',
        help='URL to scrape (single product or category page)'
    )
    parser.add_argument(
        '--merchant',
        default='Generic',
        help='Merchant name (default: Generic). Use "mercari" or "depop" for specialized scrapers.'
    )
    parser.add_argument(
        '--pages',
        type=int,
        default=1,
        help='Number of pages to scrape for multi-page scraping (default: 1)'
    )
    parser.add_argument(
        '--selenium',
        action='store_true',
        help='Use Selenium for JavaScript-rendered content'
    )
    parser.add_argument(
        '--output',
        default=None,
        help='Output file path (default: scraped_data/inventory_{merchant}_{timestamp})'
    )
    parser.add_argument(
        '--format',
        choices=['json', 'csv'],
        default=OUTPUT_FORMAT,
        help=f'Output format (default: {OUTPUT_FORMAT})'
    )
    parser.add_argument(
        '--title-selector',
        default='h1, .product-title, .item-title',
        help='CSS selector for product title'
    )
    parser.add_argument(
        '--price-selector',
        default='.price, .product-price, [itemprop="price"]',
        help='CSS selector for price'
    )
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)
    
    # Initialize scraper based on merchant type
    logger.info(f"Initializing scraper for merchant: {args.merchant}")
    
    merchant_lower = args.merchant.lower()
    
    if merchant_lower == 'mercari':
        scraper = MercariScraper()
    elif merchant_lower == 'depop':
        scraper = DepopScraper()
    else:
        # Use generic scraper with custom settings
        scraper = GenericEcommerceScraper(
            merchant_name=args.merchant,
            title_selector=args.title_selector,
            price_selector=args.price_selector,
            use_selenium=args.selenium
        )
    
    try:
        # Scrape data
        if args.pages > 1:
            logger.info(f"Scraping {args.pages} pages from {args.url}")
            collection = scraper.scrape_multiple_pages(args.url, max_pages=args.pages)
        else:
            logger.info(f"Scraping single listing from {args.url}")
            items = scraper.scrape_listing(args.url)
            collection = InventoryCollection()
            collection.add_items(items)
        
        # Generate output filename if not provided
        if args.output is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"inventory_{args.merchant}_{timestamp}.{args.format}"
            output_path = output_dir / filename
        else:
            output_path = Path(args.output)
        
        # Save results
        logger.info(f"Saving {len(collection)} items to {output_path}")
        if args.format == 'json':
            collection.save_to_json(str(output_path))
        else:
            collection.save_to_csv(str(output_path))
        
        logger.info(f"Successfully scraped {len(collection)} items")
        logger.info(f"Output saved to: {output_path}")
        
    except Exception as e:
        logger.error(f"Scraping failed: {e}", exc_info=True)
        return 1
    finally:
        scraper.cleanup()
    
    return 0


if __name__ == '__main__':
    exit(main())
