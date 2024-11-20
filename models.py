from flask_sqlalchemy import SQLAlchemy
import random
import string
from flask_mail import Mail

# Create the Mail instance globally
mail = Mail()

db = SQLAlchemy()

class SuperAdmin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    verification_code = db.Column(db.String(6), nullable=True)

def generate_verification_code():
    """Generate a random 6-digit verification code."""
    return ''.join(random.choices(string.digits, k=6))
