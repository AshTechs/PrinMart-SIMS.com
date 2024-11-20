from flask import Blueprint, request, jsonify, render_template
from werkzeug.security import generate_password_hash
from models import db, SuperAdmin, generate_verification_code, mail
from flask_mail import Message
import smtplib
import re

# Create the Blueprint
admin_bp = Blueprint('admin', __name__)

def is_valid_email(email):
    """Validate email format."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@admin_bp.route('/SuperAdsignup', methods=['GET', 'POST'])
def register_super_admin():
    """Handle super admin registration."""
    if request.method == 'GET':
        # Render the signup form
        return render_template('SuperAdsignup.html')

    data = request.json or request.form.to_dict()

    # Extract fields from data
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    repeat_password = data.get("repeat_password", "").strip()  # Extract repeat_password

    # Validation to check if all fields are filled
    if not name or not email or not password or not repeat_password:
        return jsonify({'error': 'All fields are required!'}), 400

    # Validate that passwords match
    if password != repeat_password:
        return jsonify({'error': 'Passwords do not match!'}), 400
    
    # Check if the email already exists
    existing_admin = SuperAdmin.query.filter_by(email=email).first()
    if existing_admin:
        return jsonify({'error': 'Email already exists! Please use a different email.'}), 400
    
    try:
        hashed_password = generate_password_hash(password)
        new_admin = SuperAdmin(name=name, email=email, password=hashed_password)
        
        #Save to database
        db.session.add(new_admin)
        db.session.commit()

        # Generate and send the verification code
        verification_code = generate_verification_code()
        new_admin.verification_code = verification_code
        db.session.commit()

        msg = Message("Account Verification", recipients=[email])
        msg.body = f"Your verification code is: {verification_code}"
        mail.send(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")
        return jsonify({'error': 'Unable to send verification email. Please try again later.'}), 500
        
        # Redirect to the verification page after successful registration
        return jsonify({'message': 'Super admin registered successfully! Kindly verify your email'}), 201

    except Exception as e:
        print(f"Database error: {str(e)}")
        db.session.rollback()
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

# Verification Endpoint
@admin_bp.route('/verification/<email>', methods=['GET', 'POST'])
def verification_page(email):
    if request.method == 'GET':
        return render_template('verification.html', email=email)

    # For POST, handle the code verification
    data = request.json or request.form.to_dict()
    verification_code = data.get('verification_code', '').strip()

    # Query the admin by email
    admin = SuperAdmin.query.filter_by(email=email).first()

    if not admin:
        return jsonify({'error': 'Invalid email address.'}), 400
    if admin.verification_code != verification_code:
        return jsonify({'error': 'Invalid verification code.'}), 400

    # Clear the verification code (mark as verified)
    admin.verification_code = None
    db.session.commit()

    return jsonify({'message': 'Account successfully verified!'}), 200

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('ashbelh@gmail.com', 'wwod fsgp pejn dpma')  # Replace with your email and app password
    print("SMTP connection successful!")
    server.quit()
except Exception as e:
    print(f"SMTP connection failed: {e}")