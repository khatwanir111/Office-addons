# subscribe_presence_changes.py
# ENV: NOTIFICATION_URL, SUBSCRIPTION_CLIENT_STATE (optional)
import os, json, requests
from datetime import datetime, timedelta
from helper_auth import get_token

def run():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    expiration = (datetime.utcnow() + timedelta(days=2)).isoformat() + "Z"
    payload = {
        "changeType": "updated",
        "notificationUrl": os.environ.get("NOTIFICATION_URL", "https://your-endpoint.example.com/webhook"),
        "resource": "/communications/presences/{userId}",
        "expirationDateTime": expiration,
        "clientState": os.environ.get("SUBSCRIPTION_CLIENT_STATE", "sub-state-123")
    }
    # For user-specific resource, you should replace {userId} with the actual user id or use /users/{id}/presence
    # Example resource: "/users/{id}/presence"
    resp = requests.post("https://graph.microsoft.com/v1.0/subscriptions", headers=headers, json=payload)
    print("Subscription response:", resp.status_code, resp.text)

if __name__ == "__main__":
    run()
