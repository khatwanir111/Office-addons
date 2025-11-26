# update_user_manager.py
# ENV: USER_UPN, MANAGER_UPN
import os, requests
from helper_auth import get_token

def run():
    user_upn = os.environ.get("USER_UPN")
    manager_upn = os.environ.get("MANAGER_UPN")
    if not (user_upn and manager_upn):
        print("Set USER_UPN and MANAGER_UPN")
        return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Get manager object id
    mgr_resp = requests.get(f"https://graph.microsoft.com/v1.0/users/{manager_upn}", headers=headers)
    if not mgr_resp.ok:
        print("Manager lookup failed:", mgr_resp.status_code, mgr_resp.text)
        return
    manager_id = mgr_resp.json()["id"]

    payload = {
        "@odata.id": f"https://graph.microsoft.com/v1.0/users/{manager_id}"
    }
    resp = requests.put(f"https://graph.microsoft.com/v1.0/users/{user_upn}/manager/$ref", headers=headers, json=payload)
    print("Set manager status:", resp.status_code, resp.text)

if __name__ == "__main__":
    run()
