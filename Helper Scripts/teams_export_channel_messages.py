import requests
import json

ACCESS_TOKEN = "your-access-token"
TEAM_ID = "your-team-id"
CHANNEL_ID = "your-channel-id"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

def fetch_messages():
    url = f"https://graph.microsoft.com/v1.0/teams/{TEAM_ID}/channels/{CHANNEL_ID}/messages"
    messages = []

    while url:
        response = requests.get(url, headers=headers)
        data = response.json()

        messages.extend(data.get("value", []))
        url = data.get("@odata.nextLink")

    return messages

def save_to_file(messages):
    with open("teams_messages.json", "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2)

if __name__ == "__main__":
    msgs = fetch_messages()
    save_to_file(msgs)
    print(f"Saved {len(msgs)} messages")
