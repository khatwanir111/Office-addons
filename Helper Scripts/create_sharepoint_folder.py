# create_sharepoint_folder.py
# ENV: SITE_ID (optional, uses root), FOLDER_PATH (e.g., "/Shared Documents/Automations")
import os, requests
from helper_auth import get_token

def run():
    site_id = os.environ.get("SITE_ID")  # optional
    folder_path = os.environ.get("FOLDER_PATH", "/Shared Documents/Automations")
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    if site_id:
        base = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:"
    else:
        base = "https://graph.microsoft.com/v1.0/me/drive/root:"

    # create folder by creating an item at path with folder metadata
    create_url = f"{base}{folder_path}:/children"
    payload = {"name": folder_path.split("/")[-1], "folder": {}, "@microsoft.graph.conflictBehavior": "replace"}
    resp = requests.post(create_url, headers=headers, json=payload)
    if resp.ok:
        print("Folder created or replaced:", resp.json().get("name"))
    else:
        # fallback: try creating parent path using PUT to the folder path content
        put_resp = requests.put(f"{base}{folder_path}:/content", headers=headers, data=b"")
        print("Fallback create status:", put_resp.status_code, put_resp.text)

if __name__ == "__main__":
    run()
