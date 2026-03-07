import requests

ACCESS_TOKEN = "your-access-token"
FILE_PATH = "sample.txt"

url = "https://graph.microsoft.com/v1.0/me/drive/root:/sample.txt:/content"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

with open(FILE_PATH, "rb") as f:
    response = requests.put(url, headers=headers, data=f)

print(response.json())
