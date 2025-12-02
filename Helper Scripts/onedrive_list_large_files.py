import os
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")

USER_ID = "user@domain.com"  # or user id
SCOPES = ["https://graph.microsoft.com/.default"]
SIZE_THRESHOLD_MB = 50

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

def list_large_files():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://graph.microsoft.com/v1.0/users/{USER_ID}/drive/root/children"
    threshold_bytes = SIZE_THRESHOLD_MB * 1024 * 1024

    while url:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        for item in data.get("value", []):
            if "size" in item and item["size"] >= threshold_bytes:
                print(f"{item['name']} | {item['size'] // (1024*1024)} MB")
        url = data.get("@odata.nextLink")

if __name__ == "__main__":
    list_large_files()
