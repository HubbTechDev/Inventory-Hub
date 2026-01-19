"""
Inventory Hub Flask Backend API Application.
"""

import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from backend.config import config
from backend.models import db
from backend.routes.auth import auth_bp
from backend.routes.inventory import inventory_bp
from backend.routes.scraping import scraping_bp
from backend.routes.stats import stats_bp


def create_app(config_name=None):
    """Create and configure Flask application."""
    
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    JWTManager(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(scraping_bp)
    app.register_blueprint(stats_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request'}), 400
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'Inventory Hub API'
        }), 200
    
    # API info endpoint
    @app.route('/api', methods=['GET'])
    def api_info():
        return jsonify({
            'name': 'Inventory Hub API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'inventory': '/api/inventory',
                'scraping': '/api/scraping',
                'stats': '/api/stats'
            }
        }), 200
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


def run_dev_server():
    """Run development server."""
    app = create_app('development')
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    
    print(f"\n{'='*60}")
    print(f"🚀 Inventory Hub API Server Starting")
    print(f"{'='*60}")
    print(f"Environment: development")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"API URL: http://{host}:{port}/api")
    print(f"Health Check: http://{host}:{port}/health")
    print(f"{'='*60}\n")
    
    app.run(host=host, port=port, debug=True)


if __name__ == '__main__':
    run_dev_server()
