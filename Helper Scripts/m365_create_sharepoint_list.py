import os
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")

SCOPES = ["https://graph.microsoft.com/.default"]

SITE_ID = "YOUR_SITE_ID"  # e.g. from Graph: /sites?search=...

def get_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET,
    )
    result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" not in result:
        raise RuntimeError(f"Token error: {result.get('error_description')}")
    return result["access_token"]

def create_list(list_name="DevTasks"):
    token = get_token()
    url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/lists"

    payload = {
        "displayName": list_name,
        "columns": [
            {"name": "Status", "text": {}},
            {"name": "Owner", "personOrGroup": {}},
        ],
        "list": {"template": "genericList"},
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    print("List created:", resp.json().get("id"))

if __name__ == "__main__":
    create_list("DevTasks")
