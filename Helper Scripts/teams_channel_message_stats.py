# teams_channel_message_stats.py
# ENV: TEAM_ID, CHANNEL_ID
import os, requests, json
from helper_auth import get_token

def run():
    team = os.environ.get("TEAM_ID")
    channel = os.environ.get("CHANNEL_ID")
    if not (team and channel):
        print("Set TEAM_ID and CHANNEL_ID"); return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://graph.microsoft.com/v1.0/teams/{team}/channels/{channel}/messages?$top=50"
    total = 0
    while url:
        r = requests.get(url, headers=headers)
        if not r.ok:
            print("Messages fetch failed", r.status_code, r.text); return
        data = r.json()
        total += len(data.get("value", []))
        url = data.get("@odata.nextLink")
    out = {"team": team, "channel": channel, "messageCount": total}
    put = requests.put("https://graph.microsoft.com/v1.0/me/drive/root:/channel_message_stats.json:/content",
                       headers={**headers, "Content-Type":"application/json"}, data=json.dumps(out).encode("utf-8"))
    print("Saved channel_message_stats.json:", put.status_code, "count=", total)

if __name__ == "__main__":
    run()
