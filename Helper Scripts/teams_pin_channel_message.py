# teams_pin_channel_message.py
# ENV: TEAM_ID, CHANNEL_ID, MESSAGE_ID
import os, requests
from helper_auth import get_token

def run():
    team = os.environ.get("TEAM_ID")
    channel = os.environ.get("CHANNEL_ID")
    message = os.environ.get("MESSAGE_ID")
    if not (team and channel and message):
        print("Set TEAM_ID, CHANNEL_ID, MESSAGE_ID")
        return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    url = f"https://graph.microsoft.com/v1.0/teams/{team}/channels/{channel}/messages/{message}/pin"
    resp = requests.post(url, headers=headers)
    print("Pin status:", resp.status_code, resp.text)

if __name__ == "__main__":
    run()
