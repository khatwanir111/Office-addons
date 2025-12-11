import os
import requests
import msal
from pathlib import Path

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")
USER_ID = "user@domain.com"  # or object id
PHOTO_FILE = "photo.jpg"     # local image file

SCOPES = ["https://graph.microsoft.com/.default"]

def get_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(SCOPES)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))
    return result["access_token"]

def upload_photo():
    p = Path(PHOTO_FILE)
    if not p.exists():
        print("Photo file not found:", PHOTO_FILE); return
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "image/jpeg"}
    url = f"https://graph.microsoft.com/v1.0/users/{USER_ID}/photo/$value"
    with p.open("rb") as f:
        resp = requests.put(url, headers=headers, data=f.read())
    if resp.status_code in (200, 201, 204):
        print("Photo uploaded.")
    else:
        print("Upload failed:", resp.status_code, resp.text)

if __name__ == "__main__":
    upload_photo()
