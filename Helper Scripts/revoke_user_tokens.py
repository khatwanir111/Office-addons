# revoke_user_tokens.py
# ENV: TARGET_USER_UPN or TARGET_USER_ID
import os, requests
from helper_auth import get_token

def run():
    target_upn = os.environ.get("TARGET_USER_UPN")
    target_id = os.environ.get("TARGET_USER_ID")
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    if target_upn and not target_id:
        # fetch id
        r = requests.get(f"https://graph.microsoft.com/v1.0/users/{target_upn}", headers=headers)
        if not r.ok:
            print("User fetch failed", r.status_code, r.text); return
        target_id = r.json().get("id")

    if not target_id:
        print("Set TARGET_USER_UPN or TARGET_USER_ID"); return

    resp = requests.post(f"https://graph.microsoft.com/v1.0/users/{target_id}/revokeSignInSessions", headers=headers)
    print("Revoke response:", resp.status_code, resp.text)

if __name__ == "__main__":
    run()
