# manage_group_owners.py
# ENV: GROUP_ID, PRINCIPAL_UPN (user to add/remove), OP (add/remove)
import os, requests
from helper_auth import get_token

def run():
    group = os.environ.get("GROUP_ID")
    upn = os.environ.get("PRINCIPAL_UPN")
    op = os.environ.get("OP", "add")
    if not (group and upn):
        print("Set GROUP_ID and PRINCIPAL_UPN"); return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    # get principal id
    r = requests.get(f"https://graph.microsoft.com/v1.0/users/{upn}", headers=headers)
    if not r.ok:
        print("User not found", r.status_code, r.text); return
    principal_id = r.json()["id"]

    if op == "add":
        payload = {"@odata.id": f"https://graph.microsoft.com/v1.0/directoryObjects/{principal_id}"}
        res = requests.post(f"https://graph.microsoft.com/v1.0/groups/{group}/owners/$ref", headers=headers, json=payload)
        print("Add owner status:", res.status_code, res.text)
    else:
        res = requests.delete(f"https://graph.microsoft.com/v1.0/groups/{group}/owners/{principal_id}/$ref", headers=headers)
        print("Remove owner status:", res.status_code, res.text)

if __name__ == "__main__":
    run()
