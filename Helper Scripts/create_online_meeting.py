import os
import requests
import msal
from datetime import datetime, timedelta, timezone

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")

USER_ID = "user@domain.com"
SCOPES = ["https://graph.microsoft.com/.default"]

def get_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET,
    )
    result = app.acquire_token_for_client(SCOPES)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))
    return result["access_token"]

def create_meeting():
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    start = datetime.now(timezone.utc) + timedelta(minutes=10)
    end = start + timedelta(hours=1)

    payload = {
        "subject": "Dev Sync via API",
        "startDateTime": start.isoformat(),
        "endDateTime": end.isoformat(),
    }

    url = f"https://graph.microsoft.com/v1.0/users/{USER_ID}/onlineMeetings"
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    meeting = resp.json()

    print("Meeting created.")
    print("Subject:", meeting.get("subject"))
    print("Join URL:", meeting.get("joinWebUrl"))

if __name__ == "__main__":
    create_meeting()
