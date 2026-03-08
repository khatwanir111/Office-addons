import requests

ACCESS_TOKEN = "your-access-token"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

def get_recent_emails():
    url = "https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messages?$top=10"

    response = requests.get(url, headers=headers)
    data = response.json()

    for mail in data.get("value", []):
        subject = mail.get("subject")
        sender = mail.get("from", {}).get("emailAddress", {}).get("address")
        print(f"{subject} from {sender}")

if __name__ == "__main__":
    get_recent_emails()
