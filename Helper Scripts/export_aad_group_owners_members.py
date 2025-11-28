# export_aad_group_owners_members.py
# ENV: none
import os, json, requests
from helper_auth import get_token

def run():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    url = "https://graph.microsoft.com/v1.0/groups?$top=50"
    groups = []
    while url:
        r = requests.get(url, headers=headers)
        if not r.ok:
            print("Groups fetch failed:", r.status_code, r.text)
            return
        data = r.json()
        groups.extend(data.get("value", []))
        url = data.get("@odata.nextLink")

    report = []
    for g in groups:
        gid = g["id"]
        owners_r = requests.get(f"https://graph.microsoft.com/v1.0/groups/{gid}/owners", headers=headers)
        members_r = requests.get(f"https://graph.microsoft.com/v1.0/groups/{gid}/members", headers=headers)
        owners = owners_r.json().get("value", []) if owners_r.ok else []
        members = members_r.json().get("value", []) if members_r.ok else []
        report.append({
            "id": gid,
            "displayName": g.get("displayName"),
            "mail": g.get("mail"),
            "owners": [{"id": o.get("id"), "displayName": o.get("displayName")} for o in owners],
            "members": [{"id": m.get("id"), "displayName": m.get("displayName")} for m in members]
        })

    out = json.dumps(report, indent=2)
    put = requests.put(
        "https://graph.microsoft.com/v1.0/me/drive/root:/aad_groups_owners_members.json:/content",
        headers={"Authorization": f"Bearer {token}", "Content-Type":"application/json"},
        data=out.encode("utf-8")
    )
    print("Saved aad_groups_owners_members.json:", put.status_code)

if __name__ == "__main__":
    run()
