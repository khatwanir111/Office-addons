import os
import json
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")

SCOPES = ["https://graph.microsoft.com/.default"]
DELTA_TOKEN_FILE = "users_delta_token.json"

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

def load_delta_link():
    if not os.path.exists(DELTA_TOKEN_FILE):
        return None
    with open(DELTA_TOKEN_FILE, "r", encoding="utf-8") as f:
        return json.load(f).get("deltaLink")

def save_delta_link(link: str):
    with open(DELTA_TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump({"deltaLink": link}, f)

def sync_users_delta():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    delta_link = load_delta_link()
    url = delta_link or "https://graph.microsoft.com/v1.0/users/delta"

    all_changes = []
    while url:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        all_changes.extend(data.get("value", []))
        url = data.get("@odata.nextLink")
        delta_link = data.get("@odata.deltaLink") or delta_link

    print(f"Found {len(all_changes)} changed/new users:")
    for u in all_changes:
        print("-", u.get("id"), u.get("displayName"), u.get("userPrincipalName"))

    if delta_link:
        save_delta_link(delta_link)
        print("Delta link saved.")

if __name__ == "__main__":
    sync_users_delta()
