import requests

ACCESS_TOKEN = "your-access-token"
TEAM_ID = "your-team-id"

url = f"https://graph.microsoft.com/v1.0/teams/{TEAM_ID}/channels"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "displayName": "Development Channel",
    "description": "Channel created via Python",
    "membershipType": "standard"
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code, response.text)
