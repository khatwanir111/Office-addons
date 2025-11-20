# batch_delete_temp_files.py
import os, requests
from helper_auth import get_token

PREFIX = os.environ.get("TEMP_PREFIX", "tmp_")
DRIVE_SCOPE = os.environ.get("DRIVE_SCOPE", "me")  # 'me' or 'sites/{site-id}/drive'

def run():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    url = f"https://graph.microsoft.com/v1.0/{DRIVE_SCOPE}/drive/root/children"
    r = requests.get(url, headers=headers)
    if not r.ok:
        print("Failed to list drive:", r.status_code, r.text); return

    for item in r.json().get("value", []):
        name = item.get("name", "")
        if name.startswith(PREFIX):
            item_id = item["id"]
            delr = requests.delete(f"https://graph.microsoft.com/v1.0/{DRIVE_SCOPE}/drive/items/{item_id}", headers=headers)
            print("Deleted", name, delr.status_code)

if __name__ == "__main__":
    run()
