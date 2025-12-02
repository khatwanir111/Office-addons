import os
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")

SCOPES = ["https://graph.microsoft.com/.default"]
GROUP_ID = "YOUR_GROUP_ID"
USER_OBJECT_ID = "USER_OBJECT_ID"  # not UPN, the directory object id

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

def add_member():
    token = get_token()
    url = f"https://graph.microsoft.com/v1.0/groups/{GROUP_ID}/members/$ref"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "@odata.id": f"https://graph.microsoft.com/v1.0/directoryObjects/{USER_OBJECT_ID}"
    }
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code == 204:
        print("User added to group.")
    else:
        resp.raise_for_status()

if __name__ == "__main__":
    add_member()
