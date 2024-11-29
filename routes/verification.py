#*** from flask import Blueprint, request, jsonify, render_template, session, url_for
#from models import db, SuperAdmin, generate_verification_code, mail
#from flask_mail import Message
#import logging
#
## Create the Blueprint
#admin_bp = Blueprint('admin', __name__)
#
#mail_logger = logging.getLogger("flask_mail")
#mail_logger.setLevel(logging.DEBUG)
#handler = logging.StreamHandler()
#handler.setLevel(logging.DEBUG)
#mail_logger.setLevel(logging.DEBUG)
#handler = logging.StreamHandler()
#handler.setLevel(logging.DEBUG)
#mail_logger.addHandler(handler)
#
#@admin_bp.route('/verify_code', methods=['POST'])
#def verify_code():
#    """Verify the OTP code."""
#    data = request.json
#    email = data.get('email')
#    entered_code = data.get('verification_code')
#
#    admin = SuperAdmin.query.filter_by(email=email).first()
#
#    if not admin:
#        return jsonify({'success': False, 'error': 'Invalid email address.'}), 400
#
#    if admin.verification_code != entered_code:
#        return jsonify({'success': False, 'error': 'Invalid verification code.'}), 400
#
#    admin.verification_code = None
#    db.session.commit()
#    return jsonify({'success': True, 'redirect_url': url_for('admin.admin_dashboard')}), 200
#
#
#@admin_bp.route('/resend_code', methods=['POST'])
#def resend_verification_code():
#    """Resend a new verification code."""
#    data = request.json
#    email = data.get("email")
#
#    admin = SuperAdmin.query.filter_by(email=email).first()
#    if not admin:
#        return jsonify({'error': 'User not found.'}), 404
#
#    new_code = generate_verification_code()
#    admin.verification_code = new_code
#    db.session.commit()
#
#    msg = Message("Resend Verification Code", recipients=[email])
#    msg.body = f"Your new verification code is: {new_code}. It is valid for 120 seconds."
#    mail.send(msg)
#
#    return jsonify({'message': 'New verification code sent successfully.'}), 200
#
#
#@admin_bp.route('/admindashboard')
#def admin_dashboard():
#    """Render admin dashboard."""
#    return render_template('admindashboard.html')