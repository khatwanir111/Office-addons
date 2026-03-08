import requests

ACCESS_TOKEN = "your-access-token"
SEARCH_KEYWORD = "Dev"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

def get_users():
    url = "https://graph.microsoft.com/v1.0/users"

    response = requests.get(url, headers=headers)
    data = response.json()

    for user in data.get("value", []):
        name = user.get("displayName")
        email = user.get("mail")

        if name and SEARCH_KEYWORD.lower() in name.lower():
            print(f"{name} - {email}")

if __name__ == "__main__":
    get_users()
