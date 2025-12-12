import os
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "")
USER_UPN = "user@domain.com"
ITEM_ID = "SOURCE_ITEM_ID"
DEST_PARENT_ID = "DEST_FOLDER_ITEM_ID"
SCOPES = ["https://graph.microsoft.com/.default"]

def get_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    )
    res = app.acquire_token_for_client(SCOPES)
    if "access_token" not in res:
        raise SystemExit(res.get("error_description"))
    return res["access_token"]

def move_item(token):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"parentReference": {"id": DEST_PARENT_ID}}
    url = f"https://graph.microsoft.com/v1.0/users/{USER_UPN}/drive/items/{ITEM_ID}"
    r = requests.patch(url, headers=headers, json=payload)
    r.raise_for_status()
    print("Moved item:", r.json().get("id"))

def main():
    token = get_token()
    move_item(token)

if __name__ == "__main__":
    main()
