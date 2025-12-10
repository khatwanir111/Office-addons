import os
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "")

CHAT_ID = "YOUR_CHAT_ID"
SCOPES = ["https://graph.microsoft.com/.default"]

def get_token():
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET,
    ).acquire_token_for_client(SCOPES)["access_token"]

def get_messages():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://graph.microsoft.com/v1.0/chats/{CHAT_ID}/messages"

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    for msg in resp.json().get("value", []):
        user = msg.get("from", {}).get("user", {}).get("displayName")
        print(user, ":", msg.get("body", {}).get("content", ""))

if __name__ == "__main__":
    get_messages()
