"""
Scraping job routes.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, ScrapingJob, InventoryItem
from datetime import datetime, timezone
import sys
import os
import json
import logging
import traceback

logger = logging.getLogger(__name__)

# NOTE: Import scrapers from parent directory
# The scrapers (mercari_scraper, depop_scraper, generic_scraper) are in the project root.
# For production, consider moving scrapers into backend/ or installing as a package.
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from mercari_scraper import MercariScraper
from depop_scraper import DepopScraper
from generic_scraper import GenericEcommerceScraper

scraping_bp = Blueprint('scraping', __name__, url_prefix='/api/scraping')


def parse_scraped_datetime(timestamp_str):
    """
    Parse ISO format datetime string to UTC naive datetime.
    
    Args:
        timestamp_str: ISO format datetime string (may include timezone)
        
    Returns:
        datetime: UTC naive datetime object, or current UTC time on error
    """
    if not timestamp_str:
        return datetime.utcnow()
    
    try:
        # Handle ISO format with optional timezone
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        # Convert to UTC naive datetime for consistency
        if dt.tzinfo is not None:
            return dt.astimezone(timezone.utc).replace(tzinfo=None)
        return dt
    except (ValueError, TypeError, AttributeError):
        logger.warning(f"Failed to parse datetime '{timestamp_str}', using current time")
        return datetime.utcnow()


def mark_job_failed(job, error_msg):
    """
    Mark a scraping job as failed with error message.
    
    Args:
        job: ScrapingJob instance
        error_msg: Error message string
    """
    job.status = 'failed'
    job.error_message = error_msg
    job.completed_at = datetime.utcnow()


def get_scraper(merchant):
    """Get appropriate scraper for merchant."""
    merchant_lower = merchant.lower()
    
    if 'mercari' in merchant_lower:
        return MercariScraper()
    elif 'depop' in merchant_lower:
        return DepopScraper()
    else:
        return GenericEcommerceScraper(merchant_name=merchant)


@scraping_bp.route('/scrape', methods=['POST'])
@jwt_required()
def start_scraping():
    """Start a new scraping job."""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        url = data.get('url', '').strip()
        merchant = data.get('merchant', 'Generic').strip()
        max_pages = data.get('max_pages', 1)
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Validate max_pages
        if max_pages < 1 or max_pages > 10:
            return jsonify({'error': 'max_pages must be between 1 and 10'}), 400
        
        # Create scraping job
        job = ScrapingJob(
            user_id=current_user_id,
            merchant=merchant,
            url=url,
            status='running',
            started_at=datetime.utcnow()
        )
        db.session.add(job)
        db.session.commit()
        
        # Perform scraping
        scraped_items = []
        error_msg = None
        
        try:
            scraper = get_scraper(merchant)
            
            with scraper:
                if max_pages == 1:
                    # Single page scraping
                    items = scraper.scrape_listing(url)
                    scraped_items = items
                else:
                    # Multi-page scraping
                    collection = scraper.scrape_multiple_pages(url, max_pages=max_pages)
                    scraped_items = list(collection.items)
            
            # Save scraped items to database
            items_count = 0
            for scraped_item in scraped_items:
                # Convert scraper InventoryItem to database model
                db_item = InventoryItem(
                    user_id=current_user_id,
                    job_id=job.id,
                    title=scraped_item.title,
                    price=scraped_item.price,
                    currency=scraped_item.currency,
                    quantity=scraped_item.quantity or 1,
                    sku=scraped_item.sku,
                    description=scraped_item.description,
                    category=scraped_item.category,
                    brand=scraped_item.brand,
                    condition=scraped_item.condition,
                    image_url=scraped_item.image_url,
                    product_url=scraped_item.product_url,
                    merchant=scraped_item.merchant,
                    in_stock=scraped_item.in_stock,
                    scraped_at=parse_scraped_datetime(scraped_item.scraped_at)
                )
                
                # Handle custom fields
                if scraped_item.custom_fields:
                    db_item.custom_fields = json.dumps(scraped_item.custom_fields)
                
                db.session.add(db_item)
                items_count += 1
            
            # Update job status
            job.status = 'completed'
            job.items_scraped = items_count
            job.completed_at = datetime.utcnow()
            
        except ImportError as e:
            error_msg = f"Scraper import error: {str(e)}"
            logger.error(f"Failed to import scraper: {traceback.format_exc()}")
            mark_job_failed(job, error_msg)
        except (ConnectionError, TimeoutError) as e:
            error_msg = f"Network error during scraping: {str(e)}"
            logger.error(f"Scraping network error: {traceback.format_exc()}")
            mark_job_failed(job, error_msg)
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(f"Scraping job {job.id} failed with exception: {traceback.format_exc()}")
            mark_job_failed(job, error_msg)
        
        db.session.commit()
        
        if error_msg:
            return jsonify({
                'message': 'Scraping job failed',
                'job': job.to_dict(),
                'error': error_msg
            }), 500
        
        return jsonify({
            'message': f'Scraping completed successfully. {job.items_scraped} items scraped.',
            'job': job.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to start scraping: {str(e)}'}), 500


@scraping_bp.route('/jobs', methods=['GET'])
@jwt_required()
def list_jobs():
    """List scraping jobs for current user."""
    try:
        current_user_id = get_jwt_identity()
        
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        
        # Filter by status
        status = request.args.get('status', '').strip()
        
        # Build query
        query = ScrapingJob.query.filter_by(user_id=current_user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        # Order by created_at desc
        query = query.order_by(ScrapingJob.created_at.desc())
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        jobs = [job.to_dict() for job in pagination.items]
        
        return jsonify({
            'jobs': jobs,
            'pagination': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total_items': pagination.total,
                'total_pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to list jobs: {str(e)}'}), 500


@scraping_bp.route('/jobs/<int:job_id>', methods=['GET'])
@jwt_required()
def get_job(job_id):
    """Get details of a specific scraping job."""
    try:
        current_user_id = get_jwt_identity()
        
        job = ScrapingJob.query.filter_by(id=job_id, user_id=current_user_id).first()
        
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        # Get items from this job
        items = InventoryItem.query.filter_by(job_id=job_id).all()
        items_data = [item.to_dict() for item in items]
        
        job_data = job.to_dict()
        job_data['items'] = items_data
        
        return jsonify({'job': job_data}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get job: {str(e)}'}), 500
