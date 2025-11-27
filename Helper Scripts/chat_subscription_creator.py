# chat_subscription_creator.py
# ENV: NOTIFICATION_URL, CLIENT_STATE (optional)
import os, requests
from datetime import datetime, timedelta
from helper_auth import get_token

def run():
    notif_url = os.environ.get("NOTIFICATION_URL")
    if not notif_url:
        print("Set NOTIFICATION_URL")
        return

    client_state = os.environ.get("CLIENT_STATE", "chat-sub-state")
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    expiration = (datetime.utcnow() + timedelta(hours=1)).isoformat() + "Z"
    payload = {
        "changeType": "created,updated",
        "notificationUrl": notif_url,
        "resource": "/chats/getAllMessages",
        "expirationDateTime": expiration,
        "clientState": client_state
    }

    resp = requests.post("https://graph.microsoft.com/v1.0/subscriptions", headers=headers, json=payload)
    print("Chat subscription status:", resp.status_code, resp.text)

if __name__ == "__main__":
    run()
