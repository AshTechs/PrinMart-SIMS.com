from flask import Blueprint, request, jsonify, render_template, session, url_for
from werkzeug.security import generate_password_hash
from models import db, SuperAdmin, generate_verification_code, mail, datetime, timedelta, timezone
from flask_mail import Message
import logging
import re

# Create the Blueprint
admin_bp = Blueprint('admin', __name__)

# Logger configuration
mail_logger = logging.getLogger("flask_mail")
mail_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
mail_logger.addHandler(handler)

def is_valid_email(email):
    """Validate email format."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@admin_bp.route('/SuperAdsignup', methods=['GET', 'POST'])
def register_super_admin():
    """Handle super admin registration."""
    if request.method == 'GET':
        # Render SuperAdsignup.html
        return render_template('SuperAdsignup.html')

    data = request.json or request.form.to_dict()

    # Extract fields from data
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    repeat_password = data.get("repeat_password", "").strip()

    # Validation to check if all fields are filled
    if not name or not email or not password or not repeat_password:
        return jsonify({'error': 'All fields are required!'}), 400

    # Validate email format
    if not is_valid_email(email):
        return jsonify({'error': 'Invalid email format.'}), 400

    # Validate that passwords match
    if password != repeat_password:
        return jsonify({'error': 'Passwords do not match!'}), 400

    # Check if the email already exists
    existing_admin = SuperAdmin.query.filter_by(email=email).first()
    if existing_admin:
        return jsonify({'error': 'Email already exists! Please use a different email.'}), 400

    try:
        # Hash the password and create a new admin
        hashed_password = generate_password_hash(password)
        verification_code = generate_verification_code()
        new_admin = SuperAdmin(
            name=name,
            email=email,
            password=hashed_password,
            verification_code=verification_code
        )

        # Save to database
        db.session.add(new_admin)
        db.session.commit()

        # Send verification email
        msg = Message("Account Verification", recipients=[email])
        msg.body = f"Thank you for signing up with PrinMart School Information Management System(SIMS). Your verification code is: {verification_code}. It expires in 2 minutes." 
        mail.send(msg)
        mail_logger.debug(f"Verification email sent to {email}")

# Return success message to client
        return jsonify({'message': 'Super admin registered successfully!'}), 201
    
    except Exception as e:
        mail_logger.error(f"Database or email error: {str(e)}")
        db.session.rollback()
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@admin_bp.route('/verification/<email>', methods=['GET', 'POST'])
def verification_page(email):
    """Handle the email verification process."""
    if request.method == 'GET':
        return render_template('verification.html', email=email)

    # For POST, handle verification code submission
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

@admin_bp.route('/resend_code', methods=['POST'])
def resend_verification_code():
    """Handle resending a new verification code."""
    try:
        data = request.json or request.form.to_dict()
        email = data.get("email")

        if not email:
            return jsonify({'error': 'Email is required.'}), 400

        # Find the user in the database
        admin = SuperAdmin.query.filter_by(email=email).first()
        if not admin:
            return jsonify({'error': 'User not found.'}), 404

        # Generate a new verification code
        new_verification_code = generate_verification_code()

        # Update the user's record
        admin.verification_code = new_verification_code
        db.session.commit()

        # Send the new verification code via email
        msg = Message("Resend Verification Code", recipients=[email])
        msg.body = f"Thank you for signing up with PrinMart School Information Management System(SIMS). Your new verification code is: {new_verification_code}. It is valid for 120 seconds."
        mail.send(msg)

        return jsonify({'message': 'New verification code sent successfully.'}), 200

    except Exception as e:
        mail_logger.error(f"Error while resending code: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@admin_bp.route('/verify_code', methods=['POST'])
def verify_code():
    print("Received verification request")
    data = request.get_json()
    entered_otp = data.get('verification_code')
    generated_otp = session.get('generated_otp')

    if not generated_otp:
        return jsonify(success=False, error="No OTP generated. Request a new one."), 400

    if entered_otp == generated_otp:
        session['admin_authenticated'] = True
        session.pop('generated_otp', None)
        return jsonify(success=True, redirect_url=url_for('/admin.admindashboard')), 200
    else:
        return jsonify(success=False, error="Invalid verification code"), 400

# Example admin dashboard route
@admin_bp.route('/admindashboard')
def admin_dashboard():
    return render_template('admindashboard.html')