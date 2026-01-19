"""
Statistics routes.
"""

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, DBInventoryItem, ScrapingJob
from sqlalchemy import func
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('stats', __name__, url_prefix='/api/stats')


@bp.route('', methods=['GET'])
@jwt_required()
def get_statistics():
    """Get dashboard statistics."""
    try:
        user_id = get_jwt_identity()
        
        # Total items
        total_items = DBInventoryItem.query.filter_by(user_id=user_id).count()
        
        # Total value
        total_value = db.session.query(func.sum(DBInventoryItem.price))\
            .filter(DBInventoryItem.user_id == user_id)\
            .scalar() or 0
        
        # Items by merchant
        items_by_merchant = db.session.query(
            DBInventoryItem.merchant,
            func.count(DBInventoryItem.id).label('count')
        ).filter(DBInventoryItem.user_id == user_id)\
         .group_by(DBInventoryItem.merchant)\
         .all()
        
        merchant_stats = [
            {'merchant': m or 'Unknown', 'count': c}
            for m, c in items_by_merchant
        ]
        
        # Items by condition
        items_by_condition = db.session.query(
            DBInventoryItem.condition,
            func.count(DBInventoryItem.id).label('count')
        ).filter(DBInventoryItem.user_id == user_id)\
         .group_by(DBInventoryItem.condition)\
         .all()
        
        condition_stats = [
            {'condition': c or 'unknown', 'count': cnt}
            for c, cnt in items_by_condition
        ]
        
        # Price distribution
        price_ranges = [
            ('0-25', 0, 25),
            ('25-50', 25, 50),
            ('50-100', 50, 100),
            ('100-250', 100, 250),
            ('250+', 250, float('inf'))
        ]
        
        price_distribution = []
        for label, min_price, max_price in price_ranges:
            if max_price == float('inf'):
                count = DBInventoryItem.query.filter(
                    DBInventoryItem.user_id == user_id,
                    DBInventoryItem.price >= min_price
                ).count()
            else:
                count = DBInventoryItem.query.filter(
                    DBInventoryItem.user_id == user_id,
                    DBInventoryItem.price >= min_price,
                    DBInventoryItem.price < max_price
                ).count()
            
            if count > 0:
                price_distribution.append({'range': label, 'count': count})
        
        # Recently added items
        recent_items = DBInventoryItem.query.filter_by(user_id=user_id)\
            .order_by(DBInventoryItem.created_at.desc())\
            .limit(10)\
            .all()
        
        # Scraping job stats
        total_jobs = ScrapingJob.query.filter_by(user_id=user_id).count()
        successful_jobs = ScrapingJob.query.filter_by(
            user_id=user_id,
            status='completed'
        ).count()
        
        # Sold vs unsold items
        sold_items = DBInventoryItem.query.filter_by(
            user_id=user_id,
            is_sold=True
        ).count()
        unsold_items = total_items - sold_items
        
        return jsonify({
            'total_items': total_items,
            'total_value': round(total_value, 2),
            'items_by_merchant': merchant_stats,
            'items_by_condition': condition_stats,
            'price_distribution': price_distribution,
            'recent_items': [item.to_dict() for item in recent_items],
            'total_scraping_jobs': total_jobs,
            'successful_scraping_jobs': successful_jobs,
            'sold_items': sold_items,
            'unsold_items': unsold_items
        }), 200
        
    except Exception as e:
        logger.error(f"Get statistics error: {e}")
        return jsonify({'error': 'Failed to get statistics'}), 500
