# send_adaptive_card.py
import os, json, requests
from helper_auth import get_token

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

TEAM_ID = os.environ.get("TEAM_ID")       # set in secrets
CHANNEL_ID = os.environ.get("CHANNEL_ID") # set in secrets

adaptive_card = {
  "type": "message",
  "attachments": [
    {
      "contentType": "application/vnd.microsoft.card.adaptive",
      "content": {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.3",
        "body": [
          {"type":"TextBlock","size":"Medium","weight":"Bolder","text":"Automated Dev Card"},
          {"type":"TextBlock","text":"This is an adaptive card posted by an automated script.","wrap":True}
        ]
      }
    }
  ]
}

if not TEAM_ID or not CHANNEL_ID:
    print("TEAM_ID and CHANNEL_ID must be set in env.")
else:
    url = f"https://graph.microsoft.com/v1.0/teams/{TEAM_ID}/channels/{CHANNEL_ID}/messages"
    resp = requests.post(url, headers=headers, json=adaptive_card)
    print(resp.status_code, resp.text)
