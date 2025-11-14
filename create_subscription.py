# create_subscription.py
import os, json, requests
from helper_auth import get_token
from datetime import datetime, timedelta

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Subscribe to drive root changes (change resource as needed: /me/messages, /users/{id}/events, etc.)
expiration = (datetime.utcnow() + timedelta(days=2)).isoformat() + "Z"  # max depends on resource
payload = {
    "changeType": "created,updated,deleted",
    "notificationUrl": os.environ.get("NOTIFICATION_URL", "https://your-ngrok-or-endpoint.example.com/webhook"),
    "resource": "/me/drive/root",
    "expirationDateTime": expiration,
    "clientState": "secret-opaque-value"
}

resp = requests.post("https://graph.microsoft.com/v1.0/subscriptions", headers=headers, json=payload)
print(resp.status_code, resp.text)
