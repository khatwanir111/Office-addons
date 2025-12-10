import os
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "")

SCOPES = ["https://graph.microsoft.com/.default"]

def get_token():
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    ).acquire_token_for_client(SCOPES)["access_token"]

def list_roles():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://graph.microsoft.com/v1.0/directoryRoles"

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    for r in resp.json().get("value", []):
        print(r.get("id"), "|", r.get("displayName"))

if __name__ == "__main__":
    list_roles()
