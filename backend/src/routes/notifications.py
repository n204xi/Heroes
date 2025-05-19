from fastapi import APIRouter, Request
from datetime import datetime
import threading
from src.services.db import db

router = APIRouter()

# In-memory storage for notifications (for demonstration purposes)
notifications = []

def send_proactive_message(user_id, message):
    # Logic to send a proactive message to the user
    # This could be an email, SMS, or push notification
    print(f"Sending proactive message to {user_id}: {message}")

@router.post('/notify')
async def notify_user(request: Request):
    data = await request.json()
    user_id = data.get('user_id')
    message = data.get('message')

    if not user_id or not message:
        return {"error": "User ID and message are required"}

    # Store the notification
    notifications.append({
        'user_id': user_id,
        'message': message,
        'timestamp': datetime.now().isoformat()
    })

    # Send the proactive message in a separate thread
    threading.Thread(target=send_proactive_message, args=(user_id, message)).start()

    return {"status": "Notification sent"}

@router.get('/notifications')
async def get_notifications():
    return notifications