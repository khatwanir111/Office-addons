import os
import requests
import msal
from datetime import datetime, timedelta, timezone

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")

SCOPES = ["https://graph.microsoft.com/.default"]

USER_ID = "user@domain.com"  # or user id

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

def list_upcoming_events(top=10):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    now = datetime.now(timezone.utc)
    end = now + timedelta(days=7)
    params = {
        "startDateTime": now.isoformat(),
        "endDateTime": end.isoformat(),
        "$orderby": "start/dateTime",
        "$top": str(top),
    }

    url = f"https://graph.microsoft.com/v1.0/users/{USER_ID}/calendarView"
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    events = resp.json().get("value", [])

    for e in events:
        print(
            f"{e.get('start', {}).get('dateTime')} | "
            f"{e.get('subject')} | "
            f"{e.get('location', {}).get('displayName', '')}"
        )

if __name__ == "__main__":
    list_upcoming_events(10)
