import os
import requests
import msal
from datetime import datetime, timedelta

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")
USER_ID = "user@domain.com"  # user whose drive you want to subscribe to
NOTIFICATION_URL = "https://your-public-hook.example.com/notify"  # must be publicly accessible
SCOPES = ["https://graph.microsoft.com/.default"]

def get_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(SCOPES)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))
    return result["access_token"]

def create_subscription():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    expiration = (datetime.utcnow() + timedelta(minutes=60)).isoformat() + "Z"  # max usually 4230 minutes for some resources; adjust per resource
    payload = {
        "changeType": "created,updated,deleted",
        "notificationUrl": NOTIFICATION_URL,
        "resource": f"users/{USER_ID}/drive/root",
        "expirationDateTime": expiration,
        "clientState": "secretClientValue"
    }
    url = "https://graph.microsoft.com/v1.0/subscriptions"
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    print("Subscription created:", resp.json())

if __name__ == "__main__":
    create_subscription()
