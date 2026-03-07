import requests

ACCESS_TOKEN = "your-access-token"

url = "https://graph.microsoft.com/v1.0/me/drive/root/children"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "name": "ProjectFolder",
    "folder": {},
    "@microsoft.graph.conflictBehavior": "rename"
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
