# get_file_thumbnails.py
# ENV: FOLDER_PATH (optional e.g. "/Documents"), DRIVE_SCOPE (optional, default 'me')
import os, requests
from helper_auth import get_token

def run():
    folder = os.environ.get("FOLDER_PATH", "")
    drive_scope = os.environ.get("DRIVE_SCOPE", "me")  # 'me' or 'sites/{site-id}/drive'
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    if folder:
        url = f"https://graph.microsoft.com/v1.0/{drive_scope}/drive/root:{folder}:/children"
    else:
        url = f"https://graph.microsoft.com/v1.0/{drive_scope}/drive/root/children"

    r = requests.get(url, headers=headers)
    if not r.ok:
        print("List failed", r.status_code, r.text); return
    for item in r.json().get("value", []):
        if item.get("file"):
            item_id = item["id"]
            thumb = requests.get(f"https://graph.microsoft.com/v1.0/{drive_scope}/drive/items/{item_id}/thumbnails/0/medium/content", headers=headers)
            if thumb.ok:
                name = item["name"]
                put_name = f"thumb_{name}"
                requests.put(f"https://graph.microsoft.com/v1.0/me/drive/root:/{put_name}:/content",
                             headers={**headers, "Content-Type":"image/jpeg"}, data=thumb.content)
                print("Saved thumbnail for", name)
            else:
                print("No thumbnail for", item.get("name"))

if __name__ == "__main__":
    run()
