import requests

ACCESS_TOKEN = "your-access-token"
TEAM_ID = "your-team-id"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

def list_channels():
    url = f"https://graph.microsoft.com/v1.0/teams/{TEAM_ID}/channels"

    response = requests.get(url, headers=headers)
    data = response.json()

    for channel in data.get("value", []):
        print(channel.get("displayName"), "-", channel.get("description"))

if __name__ == "__main__":
    list_channels()
