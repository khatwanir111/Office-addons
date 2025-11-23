# export_sharepoint_list_to_csv.py
# ENV: SITE_ID (optional), LIST_NAME (required)
import os, requests, io, csv
from helper_auth import get_token

def run():
    site = os.environ.get("SITE_ID")
    list_name = os.environ.get("LIST_NAME")
    if not list_name:
        print("Set LIST_NAME"); return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    base = f"https://graph.microsoft.com/v1.0/sites/{site}" if site else "https://graph.microsoft.com/v1.0/sites/root"

    # find the list
    lists = requests.get(f"{base}/lists", headers=headers).json().get("value", [])
    lst = next((l for l in lists if l.get("displayName")==list_name), None)
    if not lst:
        print("List not found"); return
    list_id = lst["id"]

    # get items
    items = requests.get(f"{base}/lists/{list_id}/items?$expand=fields", headers=headers).json().get("value", [])
    buf = io.StringIO()
    writer = None
    for it in items:
        fields = it.get("fields", {})
        if writer is None:
            writer = csv.DictWriter(buf, fieldnames=list(fields.keys()))
            writer.writeheader()
        writer.writerow(fields)
    content = buf.getvalue().encode("utf-8")
    put = requests.put("https://graph.microsoft.com/v1.0/me/drive/root:/list_export.csv:/content", headers={**headers, "Content-Type":"text/csv"}, data=content)
    print("Saved list_export.csv:", put.status_code)

if __name__ == "__main__":
    run()
