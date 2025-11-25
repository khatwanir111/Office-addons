# create_dynamic_group.py
# ENV: GROUP_DISPLAY_NAME, RULE (dynamic membership rule syntax)
import os, requests
from helper_auth import get_token
import json

def run():
    name = os.environ.get("GROUP_DISPLAY_NAME")
    rule = os.environ.get("RULE")  # e.g., 'user.department -eq "Engineering"'
    if not (name and rule):
        print("Set GROUP_DISPLAY_NAME and RULE"); return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    payload = {
        "displayName": name,
        "mailEnabled": False,
        "mailNickname": name.replace(" ", "")[:64],
        "securityEnabled": True,
        "groupTypes": ["DynamicMembership"],
        "membershipRule": rule,
        "membershipRuleProcessingState":"On"
    }
    r = requests.post("https://graph.microsoft.com/v1.0/groups", headers=headers, json=payload)
    print("Create dynamic group:", r.status_code, r.text)

if __name__ == "__main__":
    run()
