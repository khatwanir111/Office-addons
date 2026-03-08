import requests

ACCESS_TOKEN = "your-access-token"
TEAM_ID = "your-team-id"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def create_channel(name):
    url = f"https://graph.microsoft.com/v1.0/teams/{TEAM_ID}/channels"

    payload = {
        "displayName": name,
        "description": "Created using Python automation",
        "membershipType": "standard"
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def get_messages(channel_id):
    url = f"https://graph.microsoft.com/v1.0/teams/{TEAM_ID}/channels/{channel_id}/messages"

    response = requests.get(url, headers=headers)
    data = response.json()

    for msg in data.get("value", []):
        print(msg.get("body", {}).get("content"))

if __name__ == "__main__":
    channel = create_channel("Automation Channel")
    if "id" in channel:
        get_messages(channel["id"])
