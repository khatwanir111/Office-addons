import os
import requests
import msal
import time

TENANT_ID = os.getenv("M365_TENANT_ID", "")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "")
TEAM_DISPLAY_NAME = "Dev Team via API"
TEAM_DESCRIPTION = "Created programmatically"
MEMBER_OBJECT_IDS = ["USER_OBJECT_ID_1", "USER_OBJECT_ID_2"]  # list of user object ids
SCOPES = ["https://graph.microsoft.com/.default"]

def get_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    )
    res = app.acquire_token_for_client(SCOPES)
    if "access_token" not in res:
        raise SystemExit(res.get("error_description"))
    return res["access_token"]

def create_group(token):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "displayName": TEAM_DISPLAY_NAME,
        "description": TEAM_DESCRIPTION,
        "mailEnabled": True,
        "securityEnabled": False,
        "groupTypes": ["Unified"],
        "mailNickname": TEAM_DISPLAY_NAME.replace(" ", "").lower()
    }
    r = requests.post("https://graph.microsoft.com/v1.0/groups", headers=headers, json=payload)
    r.raise_for_status()
    return r.json()["id"]

def create_team_from_group(token, group_id):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"memberSettings": {"allowCreateUpdateChannels": True}}
    r = requests.put(f"https://graph.microsoft.com/v1.0/groups/{group_id}/team", headers=headers, json=payload)
    # Creation is async; 202 Accepted expected
    if r.status_code not in (200, 201, 202):
        r.raise_for_status()
    return r

def add_member_to_group(token, group_id, user_id):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"@odata.id": f"https://graph.microsoft.com/v1.0/users/{user_id}"}
    r = requests.post(f"https://graph.microsoft.com/v1.0/groups/{group_id}/members/$ref", headers=headers, json=payload)
    if r.status_code not in (204, 201):
        r.raise_for_status()

def main():
    token = get_token()
    group_id = create_group(token)
    print("Group created:", group_id)
    # add members
    for u in MEMBER_OBJECT_IDS:
        add_member_to_group(token, group_id, u)
    print("Members added, creating team...")
    create_team_from_group(token, group_id)
    print("Team creation requested (async). Allow a minute for provisioning.")

if __name__ == "__main__":
    main()
