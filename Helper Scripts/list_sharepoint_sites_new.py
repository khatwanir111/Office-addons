import requests

ACCESS_TOKEN = "your-access-token"

url = "https://graph.microsoft.com/v1.0/sites?search=*"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

response = requests.get(url, headers=headers)
print(response.json())
