import requests

ACCESS_TOKEN = "your-access-token"
KEYWORD = "Invoice"
DEST_FOLDER_ID = "destination-folder-id"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def fetch_emails():
    url = "https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messages"
    response = requests.get(url, headers=headers)
    return response.json().get("value", [])

def move_email(msg_id):
    url = f"https://graph.microsoft.com/v1.0/me/messages/{msg_id}/move"
    payload = {"destinationId": DEST_FOLDER_ID}
    requests.post(url, headers=headers, json=payload)

def process():
    for mail in fetch_emails():
        subject = mail.get("subject", "")
        if KEYWORD.lower() in subject.lower():
            move_email(mail["id"])
            print(f"Moved: {subject}")

if __name__ == "__main__":
    process()
