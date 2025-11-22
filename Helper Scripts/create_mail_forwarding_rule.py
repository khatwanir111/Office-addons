# create_mail_forwarding_rule.py
# ENV: FORWARD_TO_EMAIL, SENDER_FILTER (e.g., 'alerts@example.com')
import os, requests
from helper_auth import get_token

def run():
    forward_to = os.environ.get("FORWARD_TO_EMAIL")
    sender = os.environ.get("SENDER_FILTER")
    if not forward_to or not sender:
        print("Set FORWARD_TO_EMAIL and SENDER_FILTER in env"); return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    rule = {
        "displayName": f"Forward_{sender}_to_{forward_to}",
        "sequence": 1,
        "isEnabled": True,
        "conditions": {"senderContains": [sender]},
        "actions": {"forwardTo": [{"emailAddress": {"address": forward_to}}]}
    }

    resp = requests.post("https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules", headers=headers, json=rule)
    print("Create rule response:", resp.status_code, resp.text)

if __name__ == "__main__":
    run()
