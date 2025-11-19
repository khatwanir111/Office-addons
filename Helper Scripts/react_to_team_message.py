# react_to_team_message.py
import os, requests
from helper_auth import get_token

def run():
    team = os.environ.get("TEAM_ID")
    channel = os.environ.get("CHANNEL_ID")
    message = os.environ.get("MESSAGE_ID")
    reaction = os.environ.get("REACTION", "like")  # supported values vary
    if not (team and channel and message):
        print("Set TEAM_ID, CHANNEL_ID, MESSAGE_ID"); return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    payload = {"reactionType": reaction}
    url = f"https://graph.microsoft.com/v1.0/teams/{team}/channels/{channel}/messages/{message}/replies"
    # Graph doesn't expose a direct "react" endpoint for channel messages in all tenants;
    # often you add a reaction via /messages/{id}/reactions. Try that:
    react_url = f"https://graph.microsoft.com/v1.0/teams/{team}/channels/{channel}/messages/{message}/reactions"
    resp = requests.post(react_url, headers=headers, json=payload)
    print("Reaction status:", resp.status_code, resp.text)

if __name__ == "__main__":
    run()
