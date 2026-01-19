"""
Database models for Inventory Hub application.
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User model for authentication and authorization."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    inventory_items = db.relationship('DBInventoryItem', backref='user', lazy='dynamic', cascade='all, delete-orphan')
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
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class DBInventoryItem(db.Model):
    """Database model for inventory items."""
    
    __tablename__ = 'inventory_items'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Product information
    title = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float)
    currency = db.Column(db.String(10), default='USD')
    quantity = db.Column(db.Integer)
    sku = db.Column(db.String(100))
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    brand = db.Column(db.String(100))
    image_url = db.Column(db.String(1000))
    product_url = db.Column(db.String(1000))
    merchant = db.Column(db.String(100), index=True)
    condition = db.Column(db.String(50), default='new')
    in_stock = db.Column(db.Boolean, default=True)
    
    # Metadata
    scraped_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Additional fields
    tags = db.Column(db.String(500))  # Comma-separated tags
    notes = db.Column(db.Text)
    is_sold = db.Column(db.Boolean, default=False)
    custom_fields = db.Column(db.JSON)
    
    # Relationship
    scraping_job_id = db.Column(db.Integer, db.ForeignKey('scraping_jobs.id'))
    
    def to_dict(self):
        """Convert inventory item to dictionary."""
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
            'image_url': self.image_url,
            'product_url': self.product_url,
            'merchant': self.merchant,
            'condition': self.condition,
            'in_stock': self.in_stock,
            'scraped_at': self.scraped_at.isoformat() if self.scraped_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'tags': self.tags.split(',') if self.tags else [],
            'notes': self.notes,
            'is_sold': self.is_sold,
            'custom_fields': self.custom_fields
        }


class ScrapingJob(db.Model):
    """Model for tracking scraping jobs."""
    
    __tablename__ = 'scraping_jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Job information
    url = db.Column(db.String(1000), nullable=False)
    merchant = db.Column(db.String(100), nullable=False)
    pages = db.Column(db.Integer, default=1)
    status = db.Column(db.String(50), default='pending', index=True)  # pending, running, completed, failed
    
    # Results
    items_scraped = db.Column(db.Integer, default=0)
    error_message = db.Column(db.Text)
    
    # Timing
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Celery task ID
    task_id = db.Column(db.String(255))
    
    # Relationships
    inventory_items = db.relationship('DBInventoryItem', backref='scraping_job', lazy='dynamic')
    
    def to_dict(self):
        """Convert scraping job to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'url': self.url,
            'merchant': self.merchant,
            'pages': self.pages,
            'status': self.status,
            'items_scraped': self.items_scraped,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'task_id': self.task_id
        }
