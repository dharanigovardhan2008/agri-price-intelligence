from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config

# Import routes
from routes.prices import prices_bp
from routes.sell import sell_bp
from routes.alerts import alerts_bp

def create_app():
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(prices_bp, url_prefix='/api/prices')
    app.register_blueprint(sell_bp, url_prefix='/api/sell')
    app.register_blueprint(alerts_bp, url_prefix='/api/alerts')
    
    # Root route
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Kisan Price Intelligence API',
            'version': '1.0.0',
            'status': 'running'
        })
    
    # Health check
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy'}), 200
    
    @app.route('/debug')
    def debug():
        import os
        return jsonify({
            'DATA_GOV_API_KEY': os.getenv('DATA_GOV_API_KEY', 'NOT SET')[:10] + '...',
            'has_key': bool(os.getenv('DATA_GOV_API_KEY'))
    })
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(Config.PORT) if hasattr(Config, 'PORT') else 5000
    app.run(host='0.0.0.0', port=port, debug=Config.DEBUG)