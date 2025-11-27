# assign_retention_label_to_file.py
# ENV: ITEM_PATH (e.g. "/Docs/file.txt"), LABEL_ID (compliance label id)
import os, requests
from helper_auth import get_token

def run():
    path = os.environ.get("ITEM_PATH")
    label_id = os.environ.get("LABEL_ID")
    if not (path and label_id):
        print("Set ITEM_PATH and LABEL_ID")
        return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Get item id
    item = requests.get(f"https://graph.microsoft.com/v1.0/me/drive/root:{path}", headers=headers)
    if not item.ok:
        print("File not found:", item.status_code, item.text)
        return
    item_id = item.json()["id"]

    payload = {"complianceTag": label_id}
    resp = requests.patch(f"https://graph.microsoft.com/v1.0/me/drive/items/{item_id}", headers=headers, json=payload)
    print("Assign label status:", resp.status_code, resp.text)

if __name__ == "__main__":
    run()
