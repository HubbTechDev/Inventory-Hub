"""
Inventory management routes.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, InventoryItem
from datetime import datetime
import json

inventory_bp = Blueprint('inventory', __name__, url_prefix='/api/inventory')


@inventory_bp.route('', methods=['GET'])
@jwt_required()
def list_inventory():
    """List inventory items with pagination, search, and filters."""
    try:
        current_user_id = get_jwt_identity()
        
        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        
        # Search parameter
        search = request.args.get('search', '').strip()
        
        # Filter parameters
        merchant = request.args.get('merchant', '').strip()
        category = request.args.get('category', '').strip()
        condition = request.args.get('condition', '').strip()
        in_stock = request.args.get('in_stock', '').strip()
        
        # Sort parameters
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        
        # Build query
        query = InventoryItem.query.filter_by(user_id=current_user_id)
        
        # Apply search
        if search:
            search_pattern = f'%{search}%'
            query = query.filter(
                (InventoryItem.title.ilike(search_pattern)) |
                (InventoryItem.description.ilike(search_pattern)) |
                (InventoryItem.sku.ilike(search_pattern))
            )
        
        # Apply filters
        if merchant:
            query = query.filter_by(merchant=merchant)
        if category:
            query = query.filter_by(category=category)
        if condition:
            query = query.filter_by(condition=condition)
        if in_stock:
            stock_bool = in_stock.lower() == 'true'
            query = query.filter_by(in_stock=stock_bool)
        
        # Apply sorting
        if hasattr(InventoryItem, sort_by):
            order_column = getattr(InventoryItem, sort_by)
            if sort_order.lower() == 'desc':
                query = query.order_by(order_column.desc())
            else:
                query = query.order_by(order_column.asc())
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        items = [item.to_dict() for item in pagination.items]
        
        return jsonify({
            'items': items,
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
        return jsonify({'error': f'Failed to list inventory: {str(e)}'}), 500


@inventory_bp.route('/<int:item_id>', methods=['GET'])
@jwt_required()
def get_inventory_item(item_id):
    """Get a single inventory item."""
    try:
        current_user_id = get_jwt_identity()
        
        item = InventoryItem.query.filter_by(id=item_id, user_id=current_user_id).first()
        
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        return jsonify({'item': item.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get item: {str(e)}'}), 500


@inventory_bp.route('', methods=['POST'])
@jwt_required()
def create_inventory_item():
    """Create a new inventory item manually."""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        title = data.get('title', '').strip()
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        
        # Create new item
        item = InventoryItem(
            user_id=current_user_id,
            title=title,
            price=data.get('price'),
            currency=data.get('currency', 'USD'),
            quantity=data.get('quantity', 1),
            sku=data.get('sku'),
            description=data.get('description'),
            category=data.get('category'),
            brand=data.get('brand'),
            condition=data.get('condition', 'new'),
            image_url=data.get('image_url'),
            product_url=data.get('product_url'),
            merchant=data.get('merchant'),
            in_stock=data.get('in_stock', True)
        )
        
        # Handle custom fields
        if data.get('custom_fields'):
            item.custom_fields = json.dumps(data['custom_fields'])
        
        db.session.add(item)
        db.session.commit()
        
        return jsonify({
            'message': 'Item created successfully',
            'item': item.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create item: {str(e)}'}), 500


@inventory_bp.route('/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_inventory_item(item_id):
    """Update an existing inventory item."""
    try:
        current_user_id = get_jwt_identity()
        
        item = InventoryItem.query.filter_by(id=item_id, user_id=current_user_id).first()
        
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update fields
        updatable_fields = [
            'title', 'price', 'currency', 'quantity', 'sku', 
            'description', 'category', 'brand', 'condition',
            'image_url', 'product_url', 'merchant', 'in_stock'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(item, field, data[field])
        
        # Handle custom fields
        if 'custom_fields' in data:
            if data['custom_fields']:
                item.custom_fields = json.dumps(data['custom_fields'])
            else:
                item.custom_fields = None
        
        item.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Item updated successfully',
            'item': item.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update item: {str(e)}'}), 500


@inventory_bp.route('/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_inventory_item(item_id):
    """Delete an inventory item."""
    try:
        current_user_id = get_jwt_identity()
        
        item = InventoryItem.query.filter_by(id=item_id, user_id=current_user_id).first()
        
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        db.session.delete(item)
        db.session.commit()
        
        return jsonify({'message': 'Item deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete item: {str(e)}'}), 500
