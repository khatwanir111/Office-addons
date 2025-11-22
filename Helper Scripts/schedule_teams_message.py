# schedule_teams_message.py
# ENV: TEAM_ID, CHANNEL_ID, SEND_AT_ISO (e.g., 2025-12-01T10:00:00Z)
import os, time, requests
from datetime import datetime, timezone
from helper_auth import get_token

def run():
    team = os.environ.get("TEAM_ID")
    channel = os.environ.get("CHANNEL_ID")
    send_at = os.environ.get("SEND_AT_ISO")
    content = os.environ.get("MSG_CONTENT", "Automated scheduled message")

    if not (team and channel and send_at):
        print("Set TEAM_ID, CHANNEL_ID, SEND_AT_ISO"); return

    send_dt = datetime.fromisoformat(send_at.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    wait_seconds = (send_dt - now).total_seconds()
    if wait_seconds > 0:
        print(f"Waiting {int(wait_seconds)}s to post message...")
        time.sleep(min(wait_seconds, 3600))  # sleep but cap per-run to avoid long blocking; CI should schedule appropriately

    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"body": {"content": content}}
    resp = requests.post(f"https://graph.microsoft.com/v1.0/teams/{team}/channels/{channel}/messages", headers=headers, json=payload)
    print("Post status:", resp.status_code, resp.text)

if __name__ == "__main__":
    run()
