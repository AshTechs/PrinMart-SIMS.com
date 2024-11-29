from flask import Flask
from flask_cors import CORS
from models import db, mail, timedelta
from routes.admin import admin_bp

def create_app():
    """Factory function to create a Flask app."""
    app = Flask(__name__)

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sims.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '5f4fd404497ec45f1627a07a412bac49'
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=2)  # Adjust as needed


    # Email configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'ashbelh@gmail.com'
    app.config['MAIL_PASSWORD'] = 'chdz ahba unkb nkvx'
    app.config['MAIL_DEFAULT_SENDER'] = 'ashbelh@gmail.com'

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    CORS(app)

    # Register Blueprints
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Create and reset database tables
    with app.app_context():
        # Drop all existing tables
        db.drop_all()
        # Create all tables
        db.create_all()

        print(app.url_map)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
