import requests

ACCESS_TOKEN = "your-access-token"
TEAM_ID = "your-team-id"
CHANNEL_ID = "your-channel-id"
USER_ID = "user-id"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def add_member():
    url = f"https://graph.microsoft.com/v1.0/teams/{TEAM_ID}/channels/{CHANNEL_ID}/members"

    payload = {
        "@odata.type": "#microsoft.graph.aadUserConversationMember",
        "roles": ["member"],
        "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{USER_ID}')"
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        print("User added")
    else:
        print("Error:", response.text)

if __name__ == "__main__":
    add_member()
