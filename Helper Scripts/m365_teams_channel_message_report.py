import os
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")
TEAM_ID = "YOUR_TEAM_ID"

SCOPES = ["https://graph.microsoft.com/.default"]

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

def list_channels(token):
    url = f"https://graph.microsoft.com/v1.0/teams/{TEAM_ID}/channels"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json().get("value", [])

def channel_messages_report(top_messages=5):
    token = get_token()
    channels = list_channels(token)
    headers = {"Authorization": f"Bearer {token}"}

    for ch in channels:
        channel_id = ch["id"]
        display_name = ch.get("displayName")
        print(f"\n=== Channel: {display_name} ===")

        url = (
            f"https://graph.microsoft.com/v1.0/teams/{TEAM_ID}"
            f"/channels/{channel_id}/messages?$top={top_messages}"
        )
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()

        for m in resp.json().get("value", []):
            from_user = (
                m.get("from", {})
                .get("user", {})
                .get("displayName", "Unknown")
            )
            body_preview = m.get("body", {}).get("content", "")[:80].replace("\n", " ")
            print(f"- {from_user}: {body_preview}")

if __name__ == "__main__":
    channel_messages_report(top_messages=5)
