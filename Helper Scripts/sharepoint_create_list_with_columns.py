import requests

ACCESS_TOKEN = "your-access-token"
SITE_ID = "your-site-id"
LIST_NAME = "ProjectTracker"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def create_list():
    url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/lists"

    payload = {
        "displayName": LIST_NAME,
        "columns": [
            {"name": "Title", "text": {}},
            {"name": "Status", "choice": {"choices": ["Open", "In Progress", "Closed"]}},
            {"name": "Owner", "text": {}}
        ],
        "list": {"template": "genericList"}
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        print("List created successfully")
    else:
        print("Failed to create list:", response.text)

if __name__ == "__main__":
    create_list()
