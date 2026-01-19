"""
Flask application for Inventory Hub.
"""

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app(config_name='default'):
    """Application factory."""
    # Initialize Flask app
    app = Flask(__name__)
    
    # Load configuration
    from backend.config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    from backend.models import db
    db.init_app(app)
    
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Import models
    from backend.models import User, DBInventoryItem, ScrapingJob
    
    # Import and register blueprints
    from backend.routes import auth, inventory, scraping, stats
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(inventory.bp)
    app.register_blueprint(scraping.bp)
    app.register_blueprint(stats.bp)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal error: {error}")
        return {'error': 'Internal server error'}, 500
    
    return app


# Create app instance
app = create_app(os.getenv('FLASK_ENV', 'default'))

if __name__ == '__main__':
    # Create tables if they don't exist
    from backend.models import db
    with app.app_context():
        db.create_all()
    
    # Run the app
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
