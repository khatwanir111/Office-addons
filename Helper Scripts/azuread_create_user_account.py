import requests
import json

ACCESS_TOKEN = "your-access-token"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def create_user():
    url = "https://graph.microsoft.com/v1.0/users"

    payload = {
        "accountEnabled": True,
        "displayName": "Dev Test User",
        "mailNickname": "devtest",
        "userPrincipalName": "devtest@yourtenant.onmicrosoft.com",
        "passwordProfile": {
            "forceChangePasswordNextSignIn": True,
            "password": "TempPassword123!"
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        print("User created successfully")
    else:
        print("Error:", response.text)

if __name__ == "__main__":
    create_user()
