import os
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")

SITE_ID = "YOUR_SITE_ID"
DRIVE_ID = "YOUR_DRIVE_ID"  # Document library drive ID

SCOPES = ["https://graph.microsoft.com/.default"]

FOLDERS = ["Docs", "Scripts", "Logs"]

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

def create_folder(name, token):
    url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/drives/{DRIVE_ID}/root/children"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "name": name,
        "folder": {},
        "@microsoft.graph.conflictBehavior": "replace",
    }
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    print("Folder created:", name)

def main():
    token = get_token()
    for folder in FOLDERS:
        create_folder(folder, token)

if __name__ == "__main__":
    main()
