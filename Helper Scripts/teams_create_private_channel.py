# teams_create_private_channel.py
# ENV: TEAM_ID, CHANNEL_NAME, MEMBER_UPNS (comma-separated)
import os, requests
from helper_auth import get_token

def run():
    team = os.environ.get("TEAM_ID")
    ch_name = os.environ.get("CHANNEL_NAME", "Private Dev Channel")
    member_upns = [u.strip() for u in os.environ.get("MEMBER_UPNS", "").split(",") if u.strip()]
    if not team:
        print("Set TEAM_ID")
        return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    # Resolve members to user IDs
    members = []
    for upn in member_upns:
        r = requests.get(f"https://graph.microsoft.com/v1.0/users/{upn}", headers=headers)
        if r.ok:
            uid = r.json()["id"]
            members.append({
                "@odata.type": "#microsoft.graph.aadUserConversationMember",
                "roles": ["member"],
                "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{uid}')"
            })

    payload = {
        "displayName": ch_name,
        "description": "Private channel created by automation",
        "membershipType": "private",
        "members": members
    }

    resp = requests.post(f"https://graph.microsoft.com/v1.0/teams/{team}/channels", headers=headers, json=payload)
    print("Create private channel status:", resp.status_code, resp.text)

if __name__ == "__main__":
    run()
