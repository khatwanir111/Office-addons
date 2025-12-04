import os
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")

SCOPES = ["https://graph.microsoft.com/.default"]

USER_ID = "USER_OBJECT_ID"        # target user (object id)
MANAGER_ID = "MANAGER_OBJECT_ID"  # manager user (object id)

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

def set_manager():
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "@odata.id": f"https://graph.microsoft.com/v1.0/users/{MANAGER_ID}"
    }

    url = f"https://graph.microsoft.com/v1.0/users/{USER_ID}/manager/$ref"
    resp = requests.put(url, headers=headers, json=payload)
    if resp.status_code in (200, 204):
        print("Manager updated.")
    else:
        resp.raise_for_status()

if __name__ == "__main__":
    set_manager()
