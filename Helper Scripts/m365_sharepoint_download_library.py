import os
import requests
import msal
from pathlib import Path

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")

SCOPES = ["https://graph.microsoft.com/.default"]

SITE_ID = "YOUR_SITE_ID"
DRIVE_ID = "YOUR_DRIVE_ID"  # Doc library drive id
DOWNLOAD_DIR = Path("sp_library_download")

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

def list_drive_items(token, parent="root"):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/drives/{DRIVE_ID}/root/children" \
        if parent == "root" else \
        f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/drives/{DRIVE_ID}/items/{parent}/children"
    items = []

    while url:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        items.extend(data.get("value", []))
        url = data.get("@odata.nextLink")

    return items

def download_item(token, item, base_path: Path):
    headers = {"Authorization": f"Bearer {token}"}
    if "folder" in item:
        folder_path = base_path / item["name"]
        folder_path.mkdir(parents=True, exist_ok=True)
        children = list_drive_items(token, item["id"])
        for child in children:
            download_item(token, child, folder_path)
    else:
        download_url = item["@microsoft.graph.downloadUrl"]
        resp = requests.get(download_url, headers=headers)
        resp.raise_for_status()
        file_path = base_path / item["name"]
        file_path.write_bytes(resp.content)
        print("Downloaded:", file_path)

def main():
    token = get_token()
    DOWNLOAD_DIR.mkdir(exist_ok=True)
    items = list_drive_items(token)
    for item in items:
        download_item(token, item, DOWNLOAD_DIR)

if __name__ == "__main__":
    main()
