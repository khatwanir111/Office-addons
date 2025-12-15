import os, requests, msal
from datetime import datetime, timedelta, timezone

TENANT_ID = os.getenv("M365_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET")
USERS = ["user1@domain.com", "user2@domain.com"]
SCOPES = ["https://graph.microsoft.com/.default"]

def token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET,
    )
    return app.acquire_token_for_client(SCOPES)["access_token"]

def main():
    headers = {"Authorization": f"Bearer {token()}", "Content-Type": "application/json"}
    start = datetime.now(timezone.utc) + timedelta(hours=1)
    end = start + timedelta(hours=1)

    payload = {
        "subject": "Automated Event",
        "start": {"dateTime": start.isoformat(), "timeZone": "UTC"},
        "end": {"dateTime": end.isoformat(), "timeZone": "UTC"},
    }

    for u in USERS:
        r = requests.post(
            f"https://graph.microsoft.com/v1.0/users/{u}/events",
            headers=headers,
            json=payload,
        )
        r.raise_for_status()
        print("Event created for", u)

if __name__ == "__main__":
    main()
