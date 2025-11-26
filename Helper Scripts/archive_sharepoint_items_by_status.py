# archive_sharepoint_items_by_status.py
# ENV: SITE_ID (optional), SOURCE_LIST, ARCHIVE_LIST, STATUS_COLUMN (default 'Status'), DONE_VALUE (default 'Done')
import os, requests
from helper_auth import get_token

def run():
    site_id = os.environ.get("SITE_ID")
    src_name = os.environ.get("SOURCE_LIST")
    arc_name = os.environ.get("ARCHIVE_LIST")
    status_col = os.environ.get("STATUS_COLUMN", "Status")
    done_val = os.environ.get("DONE_VALUE", "Done")
    if not (src_name and arc_name):
        print("Set SOURCE_LIST and ARCHIVE_LIST")
        return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    base = f"https://graph.microsoft.com/v1.0/sites/{site_id}" if site_id else "https://graph.microsoft.com/v1.0/sites/root"
    lists = requests.get(f"{base}/lists", headers=headers).json().get("value", [])
    get_list = lambda name: next((l for l in lists if l.get("displayName") == name), None)
    src = get_list(src_name)
    arc = get_list(arc_name)
    if not src or not arc:
        print("Source or archive list not found")
        return

    items = requests.get(f"{base}/lists/{src['id']}/items?$expand=fields", headers=headers).json().get("value", [])
    for it in items:
        fields = it.get("fields", {})
        if fields.get(status_col) == done_val:
            new_fields = fields.copy()
            # remove system fields
            for k in list(new_fields.keys()):
                if k.startswith("id") or k.startswith("ID") or k in ["ContentType", "Created", "Modified"]:
                    new_fields.pop(k, None)
            payload = {"fields": new_fields}
            ins = requests.post(f"{base}/lists/{arc['id']}/items", headers=headers, json=payload)
            if ins.ok:
                del_resp = requests.delete(f"{base}/lists/{src['id']}/items/{it['id']}", headers=headers)
                print("Archived item", it["id"], "->", ins.status_code, "del:", del_resp.status_code)
            else:
                print("Insert archive failed:", ins.status_code, ins.text)

if __name__ == "__main__":
    run()
