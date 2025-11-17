# directory_snapshot.py
import os, requests, json
from helper_auth import get_token

def run():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    def fetch_all(url):
        items = []
        while url:
            r = requests.get(url, headers=headers)
            if not r.ok:
                print("Fetch failed", r.status_code, r.text); break
            d = r.json()
            items.extend(d.get("value", []))
            url = d.get("@odata.nextLink")
        return items

    users = fetch_all("https://graph.microsoft.com/v1.0/users?$select=id,displayName,userPrincipalName")
    groups = fetch_all("https://graph.microsoft.com/v1.0/groups?$select=id,displayName,mail")

    requests.put("https://graph.microsoft.com/v1.0/me/drive/root:/directory_users.json:/content", headers={**headers, "Content-Type":"application/json"}, data=json.dumps(users))
    requests.put("https://graph.microsoft.com/v1.0/me/drive/root:/directory_groups.json:/content", headers={**headers, "Content-Type":"application/json"}, data=json.dumps(groups))
    print("Saved directory snapshot: users and groups")

if __name__ == "__main__":
    run()
