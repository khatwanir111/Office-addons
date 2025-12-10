import os
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "")

SCOPES = ["https://graph.microsoft.com/.default"]

def get_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET,
    )
    return app.acquire_token_for_client(SCOPES)["access_token"]

def create_group():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "displayName": "Dev Security Group",
        "mailEnabled": False,
        "mailNickname": "devgroup",
        "securityEnabled": True
    }

    resp = requests.post("https://graph.microsoft.com/v1.0/groups", headers=headers, json=payload)
    resp.raise_for_status()
    print("Group created:", resp.json().get("id"))

if __name__ == "__main__":
    create_group()
