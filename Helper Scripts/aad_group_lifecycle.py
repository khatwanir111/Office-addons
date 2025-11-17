# aad_group_lifecycle.py
import requests
from helper_auth import get_token
import os

def create_group_and_add_member(group_name="AutoDevGroup"):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Create group
    payload = {
        "displayName": group_name,
        "mailEnabled": False,
        "mailNickname": group_name.replace(" ", "").lower(),
        "securityEnabled": True,
        "visibility": "Private"
    }
    g = requests.post("https://graph.microsoft.com/v1.0/groups", headers=headers, json=payload)
    if not g.ok:
        print("Group creation failed:", g.status_code, g.text); return
    group = g.json()
    group_id = group["id"]
    print("Created group:", group_id)

    # Add current user as member
    me = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers).json()
    user_id = me["id"]
    add_payload = {"@odata.id": f"https://graph.microsoft.com/v1.0/directoryObjects/{user_id}"}
    add = requests.post(f"https://graph.microsoft.com/v1.0/groups/{group_id}/members/$ref", headers=headers, json=add_payload)
    print("Add member response:", add.status_code, add.text)

    # Optionally add extension data (simulate lifecycle tag)
    ext_payload = {"extension_DeveloperNotes": "auto-created-for-dev-activity"}
    # Note: extension properties require registration; this demonstrates intention
    print("Group lifecycle tag (simulation):", ext_payload)


if __name__ == "__main__":
    create_group_and_add_member()
