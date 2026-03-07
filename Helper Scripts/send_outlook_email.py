import requests

ACCESS_TOKEN = "your-access-token"

url = "https://graph.microsoft.com/v1.0/me/sendMail"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "message": {
        "subject": "Test Email",
        "body": {
            "contentType": "Text",
            "content": "Email sent from Python script."
        },
        "toRecipients": [
            {
                "emailAddress": {
                    "address": "user@example.com"
                }
            }
        ]
    }
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
