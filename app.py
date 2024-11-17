from flask import Flask
from models import db
from routes.admin_routes import admin_bp

def create_app():
    """Factory function to create a Flask app."""
    app = Flask(__name__)

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sims.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Create database tables
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
