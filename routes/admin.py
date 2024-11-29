from flask import Blueprint, request, jsonify, render_template, session, url_for
from werkzeug.security import generate_password_hash
from models import db, SuperAdmin, generate_verification_code, mail
from werkzeug.security import check_password_hash
from flask_mail import Message
import logging
import re

# Create the Blueprint
admin_bp = Blueprint('admin', __name__)

# Password validation regex
password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$"


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
        return render_template('SuperAdsignup.html')

    data = request.json or request.form.to_dict()

    # Extract fields from data
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    repeat_password = data.get("repeat_password", "").strip()

    # Validate fields
    if not name or not email or not password or not repeat_password:
        return jsonify({'error': 'All fields are required!'}), 400

    # Validates email
    if not is_valid_email(email):
        return jsonify({'error': 'Invalid email format.'}), 400

    # Check if passwords match
    if password != repeat_password:
        return jsonify({'error': 'Passwords do not match!'}), 400
    
    # Validate password with regex
    if not re.match(password_regex, password):
        return jsonify({
            'error': 'Password must be at least 6 characters long and include:\n- An uppercase letter\n- A lowercase letter\n- A number\n- A special character'
        }), 400

    existing_admin = SuperAdmin.query.filter_by(email=email).first()
    if existing_admin:
        return jsonify({'error': 'Email already exists! Please use a different email.'}), 400

    try:
        hashed_password = generate_password_hash(password)
        verification_code = generate_verification_code()
        
        # Store generated OTP in session
        session['generated_otp'] = verification_code
        
        new_admin = SuperAdmin(
            name=name,
            email=email,
            password=hashed_password,
            verification_code=verification_code
        )

        db.session.add(new_admin)
        db.session.commit()

        # Send verification email
        msg = Message("Account Verification", recipients=[email])
        msg.body = f"Thank you for signing up with PrinMart School Information Management System(SIMS). Your new verification code is: {verification_code}. It is valid for 120 seconds."
        mail.send(msg)
        mail_logger.debug(f"Verification email sent to {email}")

        redirect_url = url_for('admin.verify_code', email=email)
        return jsonify({'message': 'Super admin registered successfully!', 'redirect_url': redirect_url
        }), 201

    except Exception as e:
        mail_logger.error(f"Database or email error: {str(e)}")
        db.session.rollback()
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@admin_bp.route('/verification/<email>', methods=['GET', 'POST'])
def verification_page(email):
    if request.method == 'GET':
        return render_template('verification.html', email=email)


@admin_bp.route('/verify_code', methods=['POST'])
def verify_code():
    """Verify the OTP submitted by the user."""
    print("Received verification request")
    data = request.get_json()
    print("Request data:", data)

    if not data:
        print("Invalid or missing JSON data")
        return jsonify(success=False, error="Invalid or missing JSON data"), 400

    entered_otp = data.get('verification_code')
    print("Entered OTP:", entered_otp)

    if not entered_otp:
        print("Missing verification code")
        return jsonify(success=False, error="Missing verification code"), 400

    generated_otp = session.get('generated_otp')
    print("Generated OTP in session:", generated_otp)

    if not generated_otp:
        print("No OTP generated in session")
        return jsonify(success=False, error="No OTP generated. Request a new one."), 400

    if entered_otp == generated_otp:
        print("OTP matched successfully")
        session['admin_authenticated'] = True
        session.pop('generated_otp', None)  # Clear the OTP after successful verification
        return jsonify(success=True, redirect_url=url_for('admin.admindashboard')), 200
    else:
        print("OTP mismatch")
        return jsonify(success=False, error="Invalid verification code"), 400
    
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

        # Update the session with the new OTP
        session['generated_otp'] = new_verification_code

        # Send the new verification code via email
        msg = Message("Resend Verification Code", recipients=[email])
        msg.body = f"Thank you for signing up with PrinMart School Information Management System(SIMS). Your new verification code is: {new_verification_code}. It is valid for 120 seconds."
        mail.send(msg)

        return jsonify({'message': 'New verification code sent successfully.'}), 200

    except Exception as e:
        mail_logger.error(f"Error while resending code: {str(e)}")
        db.session.rollback()
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    
@admin_bp.route('/SuperAdlogin', methods=['GET'])
def admindashboard():
    return render_template('SuperAdlogin.html')

@admin_bp.route('/SuperAdlogin', methods=['POST'])
def super_admin_login():
    """Handle super admin login."""
    try:
        # Determine the content type of the request
        if request.content_type == 'application/json':
            data = request.json
        else:
            data = request.form.to_dict()

        # Get the admin name and password
        name = data.get('name', '').strip()
        password = data.get('password', '').strip()

        # Validate inputs
        if not name or not password:
            return jsonify({'error': 'Name and password are required!'}), 400

        # Check if the admin exists in the database
        admin = SuperAdmin.query.filter_by(name=name).first()
        if not admin:
            return jsonify({'error': 'Invalid credentials. Admin not found!'}), 401

        # Verify the password
        if not check_password_hash(admin.password, password):
            return jsonify({'error': 'Invalid credentials.'}), 401

        # Establish a session for the admin
        session['admin_id'] = admin.id
        session['admin_name'] = admin.name
        session['authenticated'] = True

        return jsonify({'message': 'Login successful!', 'redirect_url': url_for('admin.dashboard')}), 200

    except Exception as e:
        return jsonify({'error': f'An error occurred during login: {str(e)}'}), 500

@admin_bp.route('/admindashboard', methods=['GET'])
def dashboard():
    """Super Admin Dashboard."""
    if not session.get('authenticated'):
        return jsonify({'error': 'Unauthorized access! Please log in.'}), 401

    return render_template('admindashboard.html', admin_name=session.get('admin_name'))
