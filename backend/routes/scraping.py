"""
Scraping routes.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, ScrapingJob
from backend.services.scraper_service import start_scraping_task
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('scraping', __name__, url_prefix='/api/scraping')


@bp.route('/jobs', methods=['GET'])
@jwt_required()
def list_scraping_jobs():
    """List all scraping jobs for the current user."""
    try:
        user_id = get_jwt_identity()
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        pagination = ScrapingJob.query.filter_by(user_id=user_id)\
            .order_by(ScrapingJob.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'jobs': [job.to_dict() for job in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        logger.error(f"List scraping jobs error: {e}")
        return jsonify({'error': 'Failed to list scraping jobs'}), 500


@bp.route('/jobs/<int:job_id>', methods=['GET'])
@jwt_required()
def get_scraping_job(job_id):
    """Get a single scraping job."""
    try:
        user_id = get_jwt_identity()
        
        job = ScrapingJob.query.filter_by(id=job_id, user_id=user_id).first()
        
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        return jsonify({'job': job.to_dict()}), 200
        
    except Exception as e:
        logger.error(f"Get scraping job error: {e}")
        return jsonify({'error': 'Failed to get job'}), 500


@bp.route('/scrape', methods=['POST'])
@jwt_required()
def start_scraping():
    """Start a new scraping job."""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate input
        if not data or not data.get('url'):
            return jsonify({'error': 'URL is required'}), 400
        
        url = data['url']
        merchant = data.get('merchant', 'Generic')
        pages = data.get('pages', 1)
        
        # Create scraping job
        job = ScrapingJob(
            user_id=user_id,
            url=url,
            merchant=merchant,
            pages=pages,
            status='pending'
        )
        
        db.session.add(job)
        db.session.commit()
        
        # Start scraping task
        task = start_scraping_task(job.id, user_id, url, merchant, pages)
        
        # Update job with task ID
        job.task_id = task.id if hasattr(task, 'id') else None
        db.session.commit()
        
        logger.info(f"Started scraping job {job.id} for user {user_id}")
        
        return jsonify({
            'message': 'Scraping job started',
            'job': job.to_dict()
        }), 202
        
    except Exception as e:
        logger.error(f"Start scraping error: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to start scraping'}), 500
