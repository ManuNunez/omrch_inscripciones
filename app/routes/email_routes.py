from flask import Blueprint, request
from app.utils.email_utils import send_confirmation_emails_to_all

email_bp = Blueprint('email', __name__)

@email_bp.route('/send-confirmation-emails', methods=['POST'])
def send_emails():
    send_confirmation_emails_to_all()
    return "Confirmation emails sent!", 200
