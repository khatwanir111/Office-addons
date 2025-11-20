# link_file_to_list_item.py
import os, requests
from helper_auth import get_token

# Requires: SITE_ID (or uses root), LIST_NAME (existing list), FILE_PATH (OneDrive/SharePoint path)
SITE_ID = os.environ.get("SITE_ID")
LIST_NAME = os.environ.get("LIST_NAME", "ProjectDocs")
FILE_PATH = os.environ.get("FILE_PATH", "/AutoFolder/sample.pdf")  # path in drive

def run():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    if SITE_ID:
        site_base = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}"
    else:
        site_base = "https://graph.microsoft.com/v1.0/sites/root"

    # Resolve file to URL
    fresp = requests.get(f"https://graph.microsoft.com/v1.0/me/drive/root:{FILE_PATH}", headers=headers)
    if not fresp.ok:
        print("File not found", fresp.status_code, fresp.text); return
    file_obj = fresp.json()
    file_url = file_obj.get("webUrl")

    # Find list by displayName
    lists = requests.get(f"{site_base}/lists", headers=headers).json().get("value", [])
    target = next((l for l in lists if l.get("displayName")==LIST_NAME), None)
    if not target:
        print("List not found"); return
    list_id = target["id"]

    # Create item with link column (assumes a text/URL column named 'DocumentLink' exists)
    payload = {"fields": {"Title": "Linked doc: " + file_obj.get("name"), "DocumentLink": file_url}}
    resp = requests.post(f"{site_base}/lists/{list_id}/items", headers=headers, json=payload)
    print("Created list item:", resp.status_code, resp.text)

if __name__ == "__main__":
    run()
