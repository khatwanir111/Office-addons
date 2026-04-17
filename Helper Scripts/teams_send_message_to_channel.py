import requests

ACCESS_TOKEN = "your-access-token"
TEAM_ID = "your-team-id"
CHANNEL_ID = "your-channel-id"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def send_message(content):
    url = f"https://graph.microsoft.com/v1.0/teams/{TEAM_ID}/channels/{CHANNEL_ID}/messages"

    payload = {
        "body": {
            "contentType": "html",
            "content": f"<b>{content}</b>"
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        print("Message sent")
    else:
        print("Error:", response.text)

if __name__ == "__main__":
    send_message("Hello from Python automation!")
