import os
import requests
import msal
from datetime import datetime, timedelta, timezone

TENANT_ID = os.getenv("M365_TENANT_ID", "")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "")
SITE_ID = "YOUR_SITE_ID"
DRIVE_ID = "YOUR_DRIVE_ID"
SOURCE_FOLDER_ID = "SOURCE_FOLDER_ITEM_ID"  # folder id to scan
ARCHIVE_FOLDER_NAME = "Archive"
AGE_DAYS = 90
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

def list_children(token, parent_id):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/drives/{DRIVE_ID}/items/{parent_id}/children"
    items = []
    while url:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        items.extend(data.get("value", []))
        url = data.get("@odata.nextLink")
    return items

def ensure_archive(token):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/drives/{DRIVE_ID}/root/children"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    for it in r.json().get("value", []):
        if it.get("folder") and it.get("name") == ARCHIVE_FOLDER_NAME:
            return it["id"]
    payload = {"name": ARCHIVE_FOLDER_NAME, "folder": {}, "@microsoft.graph.conflictBehavior": "rename"}
    r2 = requests.post(url, headers=headers, json=payload)
    r2.raise_for_status()
    return r2.json()["id"]

def move_item(token, item_id, dest_parent_id):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"parentReference": {"id": dest_parent_id}}
    url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/drives/{DRIVE_ID}/items/{item_id}"
    r = requests.patch(url, headers=headers, json=payload)
    r.raise_for_status()

def iso_dt(s):
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except:
        return None

def main():
    token = get_token()
    archive_id = ensure_archive(token)
    cutoff = datetime.now(timezone.utc) - timedelta(days=AGE_DAYS)
    items = list_children(token, SOURCE_FOLDER_ID)
    moved = 0
    for it in items:
        if "file" not in it:
            continue
        last_mod = iso_dt(it.get("lastModifiedDateTime"))
        if last_mod and last_mod < cutoff:
            move_item(token, it["id"], archive_id)
            moved += 1
            print("Moved:", it.get("name"))
    print(f"Total moved: {moved}")

if __name__ == "__main__":
    main()
