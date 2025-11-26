# sync_group_members_to_sharepoint_list.py
# ENV: GROUP_ID, SITE_ID (optional), LIST_NAME (e.g. "GroupMembers")
import os, requests
from helper_auth import get_token

def run():
    group_id = os.environ.get("GROUP_ID")
    list_name = os.environ.get("LIST_NAME", "GroupMembers")
    site_id = os.environ.get("SITE_ID")
    if not group_id:
        print("Set GROUP_ID")
        return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    base = f"https://graph.microsoft.com/v1.0/sites/{site_id}" if site_id else "https://graph.microsoft.com/v1.0/sites/root"

    # Find or create list
    lists_resp = requests.get(f"{base}/lists", headers=headers)
    lists = lists_resp.json().get("value", [])
    target = next((l for l in lists if l.get("displayName") == list_name), None)
    if not target:
        create_payload = {
            "displayName": list_name,
            "columns": [
                {"name": "UserPrincipalName", "text": {}},
                {"name": "DisplayName", "text": {}}
            ],
            "list": {"template": "genericList"}
        }
        create_resp = requests.post(f"{base}/lists", headers=headers, json=create_payload)
        if not create_resp.ok:
            print("Failed to create list:", create_resp.status_code, create_resp.text)
            return
        target = create_resp.json()
    list_id = target["id"]

    # Get group members
    members = []
    url = f"https://graph.microsoft.com/v1.0/groups/{group_id}/members?$top=50"
    while url:
        r = requests.get(url, headers=headers)
        if not r.ok:
            print("Members fetch failed:", r.status_code, r.text)
            return
        data = r.json()
        members.extend(data.get("value", []))
        url = data.get("@odata.nextLink")

    # Clear existing items (optional)
    items = requests.get(f"{base}/lists/{list_id}/items?$expand=fields", headers=headers).json().get("value", [])
    for it in items:
        del_resp = requests.delete(f"{base}/lists/{list_id}/items/{it['id']}", headers=headers)
        print("Deleted old item:", del_resp.status_code)

    # Insert new items
    for m in members:
        if "userPrincipalName" not in m:
            continue
        fields = {
            "Title": m.get("displayName"),
            "UserPrincipalName": m.get("userPrincipalName"),
            "DisplayName": m.get("displayName")
        }
        payload = {"fields": fields}
        ins = requests.post(f"{base}/lists/{list_id}/items", headers=headers, json=payload)
        print("Inserted:", m.get("userPrincipalName"), ins.status_code)

if __name__ == "__main__":
    run()
