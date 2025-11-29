import os
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")

SCOPES = ["https://graph.microsoft.com/.default"]

LOCAL_FILE = "readme.txt"
TARGET_NAME = "readme-uploaded.txt"

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

def upload_file():
    token = get_token()
    with open(LOCAL_FILE, "rb") as f:
        content = f.read()

    url = (
        "https://graph.microsoft.com/v1.0/me/drive/root:"
        f"/{TARGET_NAME}:/content"
    )
    headers = {"Authorization": f"Bearer {token}"}

    resp = requests.put(url, headers=headers, data=content)
    resp.raise_for_status()
    print("Uploaded:", resp.json().get("id"))

if __name__ == "__main__":
    upload_file()
