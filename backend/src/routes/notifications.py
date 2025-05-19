from flask import Blueprint, request, jsonify
from datetime import datetime
import threading

notifications_bp = Blueprint('notifications', __name__)

# In-memory storage for notifications (for demonstration purposes)
notifications = []

def send_proactive_message(user_id, message):
    # Logic to send a proactive message to the user
    # This could be an email, SMS, or push notification
    print(f"Sending proactive message to {user_id}: {message}")

@notifications_bp.route('/notify', methods=['POST'])
def notify_user():
    data = request.json
    user_id = data.get('user_id')
    message = data.get('message')

    if not user_id or not message:
        return jsonify({'error': 'User ID and message are required'}), 400

    # Store the notification
    notifications.append({
        'user_id': user_id,
        'message': message,
        'timestamp': datetime.now()
    })

    # Send the proactive message in a separate thread
    threading.Thread(target=send_proactive_message, args=(user_id, message)).start()

    return jsonify({'status': 'Notification sent'}), 200

@notifications_bp.route('/notifications', methods=['GET'])
def get_notifications():
    return jsonify(notifications), 200