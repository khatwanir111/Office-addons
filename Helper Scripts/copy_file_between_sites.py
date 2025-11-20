# copy_file_between_sites.py
import os, requests, time
from helper_auth import get_token

# ENV: SOURCE_SITE_ID, SOURCE_PATH (e.g. "/Shared Documents/file.txt"), DEST_SITE_ID, DEST_FOLDER_PATH (e.g. "/Shared Documents/Migrated")
SRC_SITE = os.environ.get("SOURCE_SITE_ID")
SRC_PATH = os.environ.get("SOURCE_PATH", "/Shared Documents/sample.txt")
DST_SITE = os.environ.get("DEST_SITE_ID")
DST_FOLDER = os.environ.get("DEST_FOLDER_PATH", "/Shared Documents/Migrated")

def run():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    # get source item
    src = requests.get(f"https://graph.microsoft.com/v1.0/sites/{SRC_SITE}/drive/root:{SRC_PATH}", headers=headers)
    if not src.ok:
        print("Source item not found", src.status_code, src.text); return
    item = src.json()
    item_id = item["id"]

    # destination parent reference syntax for path
    parent_ref = {"parentReference": {"path": f"/sites/{DST_SITE}/drive/root:{DST_FOLDER}"}}
    # copy action
    copy_payload = {"parentReference": {"path": f"/sites/{DST_SITE}/drive/root:{DST_FOLDER}"}, "name": item.get("name")}
    copy_resp = requests.post(f"https://graph.microsoft.com/v1.0/sites/{SRC_SITE}/drive/items/{item_id}/copy", headers=headers, json=copy_payload)
    if copy_resp.status_code not in (202,):
        print("Copy failed or immediate:", copy_resp.status_code, copy_resp.text); return
    # If 202 accepted, Graph returns monitor-URL in Location header to poll for completion
    monitor = copy_resp.headers.get("Location")
    if monitor:
        print("Copy started; polling monitor URL...")
        while True:
            m = requests.get(monitor, headers=headers)
            if m.status_code == 200:
                print("Copy completed")
                break
            if m.status_code >= 400:
                print("Copy failed:", m.status_code, m.text); break
            time.sleep(1)
    else:
        print("Copy response:", copy_resp.status_code, copy_resp.text)

if __name__ == "__main__":
    run()
