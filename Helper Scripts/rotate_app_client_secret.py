import os
import requests
import msal
from datetime import datetime, timedelta, timezone

TENANT_ID = os.getenv("M365_TENANT_ID", "")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "")
APP_OBJECT_ID = "YOUR_APP_OBJECT_ID"  # the service principal or app object id
REMOVE_OLDER_THAN_DAYS = 90
SCOPES = ["https://graph.microsoft.com/.default"]

def get_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    )
    res = app.acquire_token_for_client(SCOPES)
    if "access_token" not in res:
        raise SystemExit(res.get("error_description"))
    return res["access_token"]

def create_secret(token, display_name="rotated-secret"):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    # set expiration in 1 year
    exp = (datetime.now(timezone.utc) + timedelta(days=365)).isoformat()
    payload = {
        "passwordCredential": {
            "displayName": display_name,
            "endDateTime": exp
        }
    }
    url = f"https://graph.microsoft.com/v1.0/applications/{APP_OBJECT_ID}/addPassword"
    r = requests.post(url, headers=headers, json=payload)
    r.raise_for_status()
    secret_text = r.json().get("secretText")
    print("New secret (store safely):", secret_text)

def remove_old_secrets(token):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://graph.microsoft.com/v1.0/applications/{APP_OBJECT_ID}"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    app = r.json()
    creds = app.get("passwordCredentials", [])
    cutoff = datetime.now(timezone.utc) - timedelta(days=REMOVE_OLDER_THAN_DAYS)
    for c in creds:
        end = c.get("endDateTime")
        if end:
            end_dt = datetime.fromisoformat(end.replace("Z", "+00:00"))
            if end_dt < cutoff:
                # remove by keyId
                kid = c.get("keyId")
                del_url = f"https://graph.microsoft.com/v1.0/applications/{APP_OBJECT_ID}/removePassword"
                payload = {"keyId": kid}
                d = requests.post(del_url, headers={**headers, "Content-Type": "application/json"}, json=payload)
                d.raise_for_status()
                print("Removed old secret:", kid)

def main():
    token = get_token()
    create_secret(token)
    try:
        remove_old_secrets(token)
    except Exception as e:
        print("Failed to remove old secrets (check permissions):", e)

if __name__ == "__main__":
    main()
