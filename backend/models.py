"""
Database models for the Inventory Hub API.
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()


class User(db.Model):
    """User model for authentication."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    inventory_items = db.relationship('InventoryItem', backref='owner', lazy='dynamic', cascade='all, delete-orphan')
    scraping_jobs = db.relationship('ScrapingJob', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the hash."""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class InventoryItem(db.Model):
    """Inventory item model."""
    
    __tablename__ = 'inventory_items'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Core fields
    title = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=True)
    currency = db.Column(db.String(3), default='USD')
    quantity = db.Column(db.Integer, default=1)
    sku = db.Column(db.String(100), nullable=True, index=True)
    
    # Descriptive fields
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable=True, index=True)
    brand = db.Column(db.String(100), nullable=True)
    condition = db.Column(db.String(50), default='new', index=True)
    
    # Media
    image_url = db.Column(db.String(500), nullable=True)
    product_url = db.Column(db.String(500), nullable=True)
    
    # Merchant info
    merchant = db.Column(db.String(100), nullable=True, index=True)
    in_stock = db.Column(db.Boolean, default=True, index=True)
    
    # Custom fields stored as JSON
    custom_fields = db.Column(db.Text, nullable=True)
    
    # Timestamps
    scraped_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to scraping job
    job_id = db.Column(db.Integer, db.ForeignKey('scraping_jobs.id'), nullable=True)
    
    def to_dict(self):
        """Convert inventory item to dictionary."""
        custom = None
        if self.custom_fields:
            try:
                custom = json.loads(self.custom_fields)
            except:
                custom = None
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'price': self.price,
            'currency': self.currency,
            'quantity': self.quantity,
            'sku': self.sku,
            'description': self.description,
            'category': self.category,
            'brand': self.brand,
            'condition': self.condition,
            'image_url': self.image_url,
            'product_url': self.product_url,
            'merchant': self.merchant,
            'in_stock': self.in_stock,
            'custom_fields': custom,
            'scraped_at': self.scraped_at.isoformat() if self.scraped_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'job_id': self.job_id
        }


class ScrapingJob(db.Model):
    """Scraping job model."""
    
    __tablename__ = 'scraping_jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Job details
    merchant = db.Column(db.String(100), nullable=False, index=True)
    url = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(50), default='pending', index=True)  # pending, running, completed, failed
    
    # Results
    items_scraped = db.Column(db.Integer, default=0)
    error_message = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    items = db.relationship('InventoryItem', backref='job', lazy='dynamic')
    
    def to_dict(self):
        """Convert scraping job to dictionary."""
        duration = None
        if self.started_at and self.completed_at:
            duration = (self.completed_at - self.started_at).total_seconds()
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'merchant': self.merchant,
            'url': self.url,
            'status': self.status,
            'items_scraped': self.items_scraped,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'duration_seconds': duration
        }
