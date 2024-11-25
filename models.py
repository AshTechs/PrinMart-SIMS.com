from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, timezone
from flask_mail import Mail
import random
import string

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
 
def is_code_valid(admin):
    """Check if the verification code is still valid."""
    if admin.code_generated_at:
        return datetime.now(timezone.utc) - admin.code_generated_at <= timedelta(seconds=120)
    return False