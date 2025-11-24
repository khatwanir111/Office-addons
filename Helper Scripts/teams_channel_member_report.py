# teams_channel_member_report.py
# ENV: TEAM_ID
import os, json, requests
from helper_auth import get_token

def run():
    team = os.environ.get("TEAM_ID")
    if not team:
        print("Set TEAM_ID"); return
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    channels = requests.get(f"https://graph.microsoft.com/v1.0/teams/{team}/channels", headers=headers).json().get("value", [])
    report = {}
    for ch in channels:
        ch_id = ch["id"]
        members = requests.get(f"https://graph.microsoft.com/v1.0/teams/{team}/channels/{ch_id}/members", headers=headers)
        report[ch.get("displayName")] = members.json().get("value", []) if members.ok else {"error": members.text}
    put = requests.put("https://graph.microsoft.com/v1.0/me/drive/root:/teams_channel_members.json:/content",
                       headers={**headers, "Content-Type":"application/json"}, data=json.dumps(report).encode("utf-8"))
    print("Saved teams channel members:", put.status_code)

if __name__ == "__main__":
    run()
