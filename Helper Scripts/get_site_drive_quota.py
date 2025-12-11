import os
import requests
import msal
import json

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")
SITE_ID = "YOUR_SITE_ID"  # site id (e.g. from /sites?search=)

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

def print_quota():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/drive"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    drive = resp.json()
    quota = drive.get("quota", {})
    print("Drive id:", drive.get("id"))
    print("Total (bytes):", quota.get("total"))
    print("Used (bytes):", quota.get("used"))
    print("Remaining (bytes):", quota.get("remaining"))
    print("Other quota details:", json.dumps(quota, indent=2))

if __name__ == "__main__":
    print_quota()
