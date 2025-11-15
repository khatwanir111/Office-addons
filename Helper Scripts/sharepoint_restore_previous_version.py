# sharepoint_restore_previous_version.py
import os, requests
from helper_auth import get_token

token = get_token()
headers = {"Authorization": f"Bearer {token}"}

# Provide the path to the file in OneDrive root
file_path = os.environ.get("SOURCE_FILE_PATH", "/AutoFolder/sample.txt")  # e.g. /AutoFolder/sample.txt

# Get item
item_resp = requests.get(f"https://graph.microsoft.com/v1.0/me/drive/root:{file_path}", headers=headers)
if not item_resp.ok:
    print("File not found:", item_resp.status_code, item_resp.text); exit(0)
item_id = item_resp.json()["id"]

# list versions
vers = requests.get(f"https://graph.microsoft.com/v1.0/me/drive/items/{item_id}/versions", headers=headers).json().get("value", [])
if len(vers) < 2:
    print("No previous versions to restore.")
else:
    prev = vers[1]  # 0 is latest, 1 is previous
    restore_resp = requests.post(f"https://graph.microsoft.com/v1.0/me/drive/items/{item_id}/versions/{prev['id']}/restoreVersion", headers=headers)
    print("Restore status:", restore_resp.status_code)
