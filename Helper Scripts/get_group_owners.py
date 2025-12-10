import os
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "")

GROUP_ID = "YOUR_GROUP_ID"
SCOPES = ["https://graph.microsoft.com/.default"]

def get_token():
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    ).acquire_token_for_client(SCOPES)["access_token"]

def list_owners():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://graph.microsoft.com/v1.0/groups/{GROUP_ID}/owners"

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    for o in resp.json().get("value", []):
        print(o.get("id"), "|", o.get("displayName"), "|", o.get("userPrincipalName"))

if __name__ == "__main__":
    list_owners()
