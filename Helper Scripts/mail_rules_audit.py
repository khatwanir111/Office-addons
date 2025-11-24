# mail_rules_audit.py
# ENV: TARGET_UPN (optional)
import os, json, requests
from helper_auth import get_token

def run():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    target = os.environ.get("TARGET_UPN")
    if target:
        url = f"https://graph.microsoft.com/v1.0/users/{target}/mailFolders/inbox/messageRules"
    else:
        url = "https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules"

    resp = requests.get(url, headers=headers)
    if not resp.ok:
        print("Failed to list rules:", resp.status_code, resp.text); return

    out = resp.json()
    put = requests.put("https://graph.microsoft.com/v1.0/me/drive/root:/mail_rules_audit.json:/content",
                       headers={**headers, "Content-Type":"application/json"}, data=json.dumps(out).encode("utf-8"))
    print("Saved mail rules audit:", put.status_code)

if __name__ == "__main__":
    run()
