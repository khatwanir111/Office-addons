import requests

ACCESS_TOKEN = "your-access-token"

url = "https://graph.microsoft.com/v1.0/me/events"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "subject": "Project Meeting",
    "start": {
        "dateTime": "2026-03-10T10:00:00",
        "timeZone": "UTC"
    },
    "end": {
        "dateTime": "2026-03-10T11:00:00",
        "timeZone": "UTC"
    }
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
