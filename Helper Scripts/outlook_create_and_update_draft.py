import requests

ACCESS_TOKEN = "your-access-token"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def create_draft():
    url = "https://graph.microsoft.com/v1.0/me/messages"

    payload = {
        "subject": "Initial Subject",
        "body": {"contentType": "Text", "content": "Draft body"},
        "toRecipients": [{"emailAddress": {"address": "user@example.com"}}]
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json().get("id")

def update_draft(message_id):
    url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}"

    payload = {"subject": "Updated Subject"}

    requests.patch(url, headers=headers, json=payload)

def send_draft(message_id):
    url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/send"
    requests.post(url, headers=headers)

if __name__ == "__main__":
    msg_id = create_draft()
    if msg_id:
        update_draft(msg_id)
        send_draft(msg_id)
        print("Draft updated and sent")
