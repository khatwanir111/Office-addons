# migrate_sharepoint_list_items.py
# ENV: SITE_ID (optional), SOURCE_LIST, DEST_LIST
import os, requests
from helper_auth import get_token

def run():
    site_id = os.environ.get("SITE_ID")
    src = os.environ.get("SOURCE_LIST")
    dst = os.environ.get("DEST_LIST")
    if not (src and dst):
        print("Set SOURCE_LIST and DEST_LIST"); return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}
    base = f"https://graph.microsoft.com/v1.0/sites/{site_id}" if site_id else "https://graph.microsoft.com/v1.0/sites/root"

    lists = requests.get(f"{base}/lists", headers=headers).json().get("value", [])
    get_list = lambda name: next((l for l in lists if l.get("displayName")==name), None)
    src_l = get_list(src)
    dst_l = get_list(dst)
    if not src_l or not dst_l:
        print("Source or destination list not found"); return

    items = requests.get(f"{base}/lists/{src_l['id']}/items?$expand=fields", headers=headers).json().get("value", [])
    for it in items:
        fields = it.get("fields", {})
        # remove read-only fields
        fields.pop("ID", None); fields.pop("Id", None)
        payload = {"fields": fields}
        r = requests.post(f"{base}/lists/{dst_l['id']}/items", headers=headers, json=payload)
        print("Migrated item:", r.status_code)
    print("Migration complete.")

if __name__ == "__main__":
    run()
