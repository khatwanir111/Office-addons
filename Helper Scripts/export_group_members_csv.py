# export_group_members_csv.py
import os, requests, csv, io
from helper_auth import get_token

GROUP_ID = os.environ.get("GROUP_ID")
GROUP_NAME = os.environ.get("GROUP_NAME")  # fallback search if GROUP_ID not set

def run():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    if not GROUP_ID and GROUP_NAME:
        search = requests.get(f"https://graph.microsoft.com/v1.0/groups?$filter=displayName eq '{GROUP_NAME}'", headers=headers).json()
        GROUPS = search.get("value", [])
        if not GROUPS:
            print("Group not found"); return
        group_id = GROUPS[0]["id"]
    else:
        group_id = GROUP_ID

    members = []
    url = f"https://graph.microsoft.com/v1.0/groups/{group_id}/members"
    while url:
        r = requests.get(url, headers=headers)
        if not r.ok:
            print("Failed to fetch members", r.status_code, r.text); return
        data = r.json()
        members.extend(data.get("value", []))
        url = data.get("@odata.nextLink")

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["id","displayName","userPrincipalName","mail"])
    for m in members:
        writer.writerow([m.get("id"), m.get("displayName"), m.get("userPrincipalName",""), m.get("mail","")])

    csv_bytes = buf.getvalue().encode("utf-8")
    put = requests.put("https://graph.microsoft.com/v1.0/me/drive/root:/group_members.csv:/content",
                       headers={**headers, "Content-Type":"text/csv"}, data=csv_bytes)
    print("Saved group_members.csv:", put.status_code)

if __name__ == "__main__":
    run()
