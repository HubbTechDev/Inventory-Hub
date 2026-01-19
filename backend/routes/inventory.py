"""
Inventory management routes.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, DBInventoryItem
from sqlalchemy import or_, and_
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('inventory', __name__, url_prefix='/api/inventory')


@bp.route('', methods=['GET'])
@jwt_required()
def list_inventory():
    """List all inventory items with pagination and filters."""
    try:
        user_id = get_jwt_identity()
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Filters
        merchant = request.args.get('merchant')
        condition = request.args.get('condition')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        search = request.args.get('search')
        is_sold = request.args.get('is_sold', type=lambda x: x.lower() == 'true')
        
        # Sorting
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        
        # Build query
        query = DBInventoryItem.query.filter_by(user_id=user_id)
        
        # Apply filters
        if merchant:
            query = query.filter(DBInventoryItem.merchant == merchant)
        
        if condition:
            query = query.filter(DBInventoryItem.condition == condition)
        
        if min_price is not None:
            query = query.filter(DBInventoryItem.price >= min_price)
        
        if max_price is not None:
            query = query.filter(DBInventoryItem.price <= max_price)
        
        if is_sold is not None:
            query = query.filter(DBInventoryItem.is_sold == is_sold)
        
        if search:
            search_filter = or_(
                DBInventoryItem.title.ilike(f'%{search}%'),
                DBInventoryItem.description.ilike(f'%{search}%'),
                DBInventoryItem.brand.ilike(f'%{search}%')
            )
            query = query.filter(search_filter)
        
        # Apply sorting
        if hasattr(DBInventoryItem, sort_by):
            order_column = getattr(DBInventoryItem, sort_by)
            if sort_order == 'desc':
                query = query.order_by(order_column.desc())
            else:
                query = query.order_by(order_column.asc())
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'items': [item.to_dict() for item in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }), 200
        
    except Exception as e:
        logger.error(f"List inventory error: {e}")
        return jsonify({'error': 'Failed to list inventory'}), 500


@bp.route('/<int:item_id>', methods=['GET'])
@jwt_required()
def get_inventory_item(item_id):
    """Get a single inventory item."""
    try:
        user_id = get_jwt_identity()
        
        item = DBInventoryItem.query.filter_by(id=item_id, user_id=user_id).first()
        
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        return jsonify({'item': item.to_dict()}), 200
        
    except Exception as e:
        logger.error(f"Get inventory item error: {e}")
        return jsonify({'error': 'Failed to get item'}), 500


@bp.route('/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_inventory_item(item_id):
    """Update an inventory item."""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        item = DBInventoryItem.query.filter_by(id=item_id, user_id=user_id).first()
        
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        # Update allowed fields
        allowed_fields = ['title', 'price', 'quantity', 'description', 'notes', 
                         'tags', 'is_sold', 'condition', 'in_stock', 'category', 'brand']
        
        for field in allowed_fields:
            if field in data:
                setattr(item, field, data[field])
        
        db.session.commit()
        
        logger.info(f"Updated inventory item {item_id}")
        
        return jsonify({
            'message': 'Item updated successfully',
            'item': item.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Update inventory item error: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to update item'}), 500


@bp.route('/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_inventory_item(item_id):
    """Delete an inventory item."""
    try:
        user_id = get_jwt_identity()
        
        item = DBInventoryItem.query.filter_by(id=item_id, user_id=user_id).first()
        
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        db.session.delete(item)
        db.session.commit()
        
        logger.info(f"Deleted inventory item {item_id}")
        
        return jsonify({'message': 'Item deleted successfully'}), 200
        
    except Exception as e:
        logger.error(f"Delete inventory item error: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to delete item'}), 500


@bp.route('/bulk-delete', methods=['POST'])
@jwt_required()
def bulk_delete_inventory():
    """Delete multiple inventory items."""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        item_ids = data.get('item_ids', [])
        
        if not item_ids:
            return jsonify({'error': 'No item IDs provided'}), 400
        
        deleted = DBInventoryItem.query.filter(
            DBInventoryItem.id.in_(item_ids),
            DBInventoryItem.user_id == user_id
        ).delete(synchronize_session=False)
        
        db.session.commit()
        
        logger.info(f"Bulk deleted {deleted} items")
        
        return jsonify({
            'message': f'Successfully deleted {deleted} items',
            'deleted': deleted
        }), 200
        
    except Exception as e:
        logger.error(f"Bulk delete error: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to delete items'}), 500
