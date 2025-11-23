# create_team_tag.py
# ENV: TEAM_ID, TAG_DISPLAY_NAME, MEMBER_UPNS (comma-separated user principal names)
import os, requests
from helper_auth import get_token

def run():
    team_id = os.environ.get("TEAM_ID")
    tag_name = os.environ.get("TAG_DISPLAY_NAME", "devs")
    members_upns = os.environ.get("MEMBER_UPNS", "")
    if not team_id:
        print("Set TEAM_ID in env"); return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    # Resolve members to user ids
    member_ids = []
    for upn in [u.strip() for u in members_upns.split(",") if u.strip()]:
        r = requests.get(f"https://graph.microsoft.com/v1.0/users/{upn}", headers=headers)
        if r.ok:
            member_ids.append(r.json().get("id"))

    members_payload = [{"userId": mid, "displayName": ""} for mid in member_ids] if member_ids else []

    payload = {"displayName": tag_name, "members": members_payload}
    resp = requests.post(f"https://graph.microsoft.com/v1.0/teams/{team_id}/tags", headers=headers, json=payload)
    print("Create tag response:", resp.status_code, resp.text)

if __name__ == "__main__":
    run()
