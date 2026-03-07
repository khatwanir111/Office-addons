import requests

ACCESS_TOKEN = "your-access-token"
TEAM_ID = "your-team-id"

url = f"https://graph.microsoft.com/v1.0/teams/{TEAM_ID}/members"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

response = requests.get(url, headers=headers)
print(response.json())
