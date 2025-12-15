import os, requests, msal
from datetime import datetime, timedelta, timezone

TENANT_ID = os.getenv("M365_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET")
INACTIVE_DAYS = 90
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
    cutoff = datetime.now(timezone.utc) - timedelta(days=INACTIVE_DAYS)
    url = "https://graph.microsoft.com/v1.0/users?$select=id,displayName,signInActivity"

    while url:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        for u in data.get("value", []):
            last = u.get("signInActivity", {}).get("lastSignInDateTime")
            if last and datetime.fromisoformat(last.replace("Z", "+00:00")) < cutoff:
                patch = requests.patch(
                    f"https://graph.microsoft.com/v1.0/users/{u['id']}",
                    headers=headers,
                    json={"accountEnabled": False},
                )
                patch.raise_for_status()
                print("Disabled:", u.get("displayName"))
        url = data.get("@odata.nextLink")

if __name__ == "__main__":
    main()
