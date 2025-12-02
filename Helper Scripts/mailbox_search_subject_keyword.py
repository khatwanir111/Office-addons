import os
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")

USER_ID = "user@domain.com"
SCOPES = ["https://graph.microsoft.com/.default"]

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

def search_by_subject(keyword="update", top=20):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ConsistencyLevel": "eventual",
    }
    url = (
        f"https://graph.microsoft.com/v1.0/users/{USER_ID}/messages"
        f"?$search=\"{keyword}\"&$top={top}"
    )

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    messages = resp.json().get("value", [])

    for m in messages:
        print(
            f"{m.get('receivedDateTime')} | "
            f"{m.get('from', {}).get('emailAddress', {}).get('address')} | "
            f"{m.get('subject')}"
        )

if __name__ == "__main__":
    search_by_subject("report", top=10)
