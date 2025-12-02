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

def set_ooo():
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    now = datetime.now(timezone.utc)
    end = now + timedelta(days=3)

    payload = {
        "automaticRepliesSetting": {
            "status": "scheduled",
            "scheduledStartDateTime": {
                "dateTime": now.isoformat(),
                "timeZone": "UTC",
            },
            "scheduledEndDateTime": {
                "dateTime": end.isoformat(),
                "timeZone": "UTC",
            },
            "internalReplyMessage": "I am currently out of office and will reply later.",
            "externalReplyMessage": "I am currently out of office and will reply when I return.",
        }
    }

    url = f"https://graph.microsoft.com/v1.0/users/{USER_ID}/mailboxSettings"
    resp = requests.patch(url, headers=headers, json=payload)
    resp.raise_for_status()
    print("Out-of-office configured.")

if __name__ == "__main__":
    set_ooo()
