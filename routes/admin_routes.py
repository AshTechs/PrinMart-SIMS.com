from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from models import db, SuperAdmin
import re

admin_bp = Blueprint('admin', __name__)

def is_valid_email(email):
    """Validate email format."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@admin_bp.route('/register', methods=['POST'])
def register_super_admin():
    """Route to register a new super admin."""
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    repeat_password = data.get('repeat_password')

    # Validations
    if not all([name, email, password, repeat_password]):
        return jsonify({'error': 'All fields are required'}), 400
    if not is_valid_email(email):
        return jsonify({'error': 'Invalid email format'}), 400
    if password != repeat_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    # Check for duplicate email
    if SuperAdmin.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    # Hash password and save admin
    hashed_password = generate_password_hash(password)
    new_admin = SuperAdmin(name=name, email=email, password=hashed_password)
    db.session.add(new_admin)
    db.session.commit()

    return jsonify({'message': 'Super admin registered successfully!'}), 201
