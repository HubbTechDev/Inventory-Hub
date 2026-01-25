"""
Scraper service for handling scraping tasks.
"""

import sys
import os
from datetime import datetime, timezone
import logging

# Add parent directory to path to import scrapers
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from mercari_scraper import MercariScraper
from depop_scraper import DepopScraper
from generic_scraper import GenericEcommerceScraper
from backend.models import db, DBInventoryItem, ScrapingJob

logger = logging.getLogger(__name__)


def start_scraping_task(job_id, user_id, url, merchant, pages=1):
    """
    Start a scraping task.
    In a production setup, this would be a Celery task.
    For now, we'll execute synchronously.
    """
    try:
        # Update job status
        job = ScrapingJob.query.get(job_id)
        if not job:
            logger.error(f"Job {job_id} not found")
            return None
        
        job.status = 'running'
        job.started_at = datetime.now(timezone.utc)
        db.session.commit()
        
        # Initialize appropriate scraper
        merchant_lower = merchant.lower()
        
        if merchant_lower == 'mercari':
            scraper = MercariScraper()
        elif merchant_lower == 'depop':
            scraper = DepopScraper()
        else:
            scraper = GenericEcommerceScraper(merchant_name=merchant)
        
        # Perform scraping
        try:
            if pages > 1:
                collection = scraper.scrape_multiple_pages(url, max_pages=pages)
            else:
                items = scraper.scrape_listing(url)
                # Import from root models module
                import sys
                sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
                from models import InventoryCollection
                collection = InventoryCollection()
                collection.add_items(items)
            
            # Save items to database
            items_saved = 0
            for item in collection:
                db_item = DBInventoryItem(
                    user_id=user_id,
                    scraping_job_id=job_id,
                    title=item.title,
                    price=item.price,
                    currency=item.currency,
                    quantity=item.quantity,
                    sku=item.sku,
                    description=item.description,
                    category=item.category,
                    brand=item.brand,
                    image_url=item.image_url,
                    product_url=item.product_url,
                    merchant=item.merchant,
                    condition=item.condition,
                    in_stock=item.in_stock,
                    scraped_at=datetime.now(timezone.utc),
                    custom_fields=item.custom_fields
                )
                db.session.add(db_item)
                items_saved += 1
            
            # Update job as completed
            job.status = 'completed'
            job.completed_at = datetime.now(timezone.utc)
            job.items_scraped = items_saved
            
            db.session.commit()
            
            logger.info(f"Scraping job {job_id} completed successfully. Saved {items_saved} items.")
            
        except Exception as scrape_error:
            logger.error(f"Scraping error for job {job_id}: {scrape_error}")
            job.status = 'failed'
            job.error_message = str(scrape_error)
            job.completed_at = datetime.now(timezone.utc)
            db.session.commit()
            
        finally:
            scraper.cleanup()
        
        # Return a simple task object
        class SimpleTask:
            def __init__(self, task_id):
                self.id = task_id
        
        return SimpleTask(str(job_id))
        
    except Exception as e:
        logger.error(f"Failed to start scraping task: {e}")
        if job:
            job.status = 'failed'
            job.error_message = str(e)
            job.completed_at = datetime.now(timezone.utc)
            db.session.commit()
        return None
