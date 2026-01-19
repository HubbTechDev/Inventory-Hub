"""
Dashboard statistics routes.
"""

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, InventoryItem, ScrapingJob
from sqlalchemy import func
from datetime import datetime, timedelta

stats_bp = Blueprint('stats', __name__, url_prefix='/api/stats')


@stats_bp.route('', methods=['GET'])
@jwt_required()
def get_stats():
    """Get dashboard statistics."""
    try:
        current_user_id = get_jwt_identity()
        
        # Total items
        total_items = InventoryItem.query.filter_by(user_id=current_user_id).count()
        
        # Items in stock
        items_in_stock = InventoryItem.query.filter_by(
            user_id=current_user_id,
            in_stock=True
        ).count()
        
        # Total inventory value
        total_value_result = db.session.query(
            func.sum(InventoryItem.price * InventoryItem.quantity)
        ).filter(
            InventoryItem.user_id == current_user_id,
            InventoryItem.price.isnot(None)
        ).scalar()
        
        total_value = float(total_value_result) if total_value_result else 0.0
        
        # Items by merchant
        items_by_merchant = db.session.query(
            InventoryItem.merchant,
            func.count(InventoryItem.id).label('count')
        ).filter(
            InventoryItem.user_id == current_user_id,
            InventoryItem.merchant.isnot(None)
        ).group_by(
            InventoryItem.merchant
        ).all()
        
        merchant_stats = [
            {'merchant': m[0], 'count': m[1]}
            for m in items_by_merchant
        ]
        
        # Items by condition
        items_by_condition = db.session.query(
            InventoryItem.condition,
            func.count(InventoryItem.id).label('count')
        ).filter(
            InventoryItem.user_id == current_user_id
        ).group_by(
            InventoryItem.condition
        ).all()
        
        condition_stats = [
            {'condition': c[0], 'count': c[1]}
            for c in items_by_condition
        ]
        
        # Items by category
        items_by_category = db.session.query(
            InventoryItem.category,
            func.count(InventoryItem.id).label('count')
        ).filter(
            InventoryItem.user_id == current_user_id,
            InventoryItem.category.isnot(None)
        ).group_by(
            InventoryItem.category
        ).limit(10).all()
        
        category_stats = [
            {'category': c[0], 'count': c[1]}
            for c in items_by_category
        ]
        
        # Recent scraping jobs
        recent_jobs = ScrapingJob.query.filter_by(
            user_id=current_user_id
        ).order_by(
            ScrapingJob.created_at.desc()
        ).limit(5).all()
        
        recent_jobs_data = [job.to_dict() for job in recent_jobs]
        
        # Total scraping jobs
        total_jobs = ScrapingJob.query.filter_by(user_id=current_user_id).count()
        
        # Successful jobs
        successful_jobs = ScrapingJob.query.filter_by(
            user_id=current_user_id,
            status='completed'
        ).count()
        
        # Failed jobs
        failed_jobs = ScrapingJob.query.filter_by(
            user_id=current_user_id,
            status='failed'
        ).count()
        
        # Items added in last 7 days
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        items_last_week = InventoryItem.query.filter(
            InventoryItem.user_id == current_user_id,
            InventoryItem.created_at >= seven_days_ago
        ).count()
        
        # Items added in last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        items_last_month = InventoryItem.query.filter(
            InventoryItem.user_id == current_user_id,
            InventoryItem.created_at >= thirty_days_ago
        ).count()
        
        return jsonify({
            'inventory': {
                'total_items': total_items,
                'items_in_stock': items_in_stock,
                'items_out_of_stock': total_items - items_in_stock,
                'total_value': round(total_value, 2),
                'items_last_week': items_last_week,
                'items_last_month': items_last_month
            },
            'merchants': merchant_stats,
            'conditions': condition_stats,
            'categories': category_stats,
            'scraping_jobs': {
                'total_jobs': total_jobs,
                'successful_jobs': successful_jobs,
                'failed_jobs': failed_jobs,
                'pending_jobs': total_jobs - successful_jobs - failed_jobs,
                'recent_jobs': recent_jobs_data
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get stats: {str(e)}'}), 500
