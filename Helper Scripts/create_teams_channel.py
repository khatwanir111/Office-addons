import os
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")
TEAM_ID = "YOUR_TEAM_ID"

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

def create_channel(name="Dev Channel", description="Channel created via script"):
    token = get_token()
    url = f"https://graph.microsoft.com/v1.0/teams/{TEAM_ID}/channels"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "displayName": name,
        "description": description,
        "membershipType": "standard",
    }
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    print("Channel created:", resp.json().get("id"))

if __name__ == "__main__":
    create_channel()
