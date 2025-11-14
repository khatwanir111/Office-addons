# move_sharepoint_file.py
import requests, json
from helper_auth import get_token

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Move a file from one folder to another in your OneDrive
# Provide source item id or path and destination parentReference
source_path = "/Documents/source.txt"     # example path in drive root
dest_folder_path = "/Documents/Archive"   # destination folder

# 1) Ensure destination folder exists (create if needed)
create_folder_url = f"https://graph.microsoft.com/v1.0/me/drive/root:{dest_folder_path}:/children"
# Creating folder requires PUT with folder metadata; simple approach: create a file there to force folder creation if absent (skip here)

# 2) Move by updating parentReference via PATCH on item
# Get source item metadata
get_item = requests.get(f"https://graph.microsoft.com/v1.0/me/drive/root:{source_path}", headers=headers)
if not get_item.ok:
    print("Source not found:", get_item.status_code, get_item.text)
else:
    item = get_item.json()
    item_id = item["id"]
    new_parent = {"parentReference": {"path": f"/drive/root:{dest_folder_path}"}}
    move_resp = requests.patch(f"https://graph.microsoft.com/v1.0/me/drive/items/{item_id}", headers=headers, json=new_parent)
    print(move_resp.status_code, move_resp.text)
