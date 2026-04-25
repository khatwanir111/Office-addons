import requests

ACCESS_TOKEN = "your-access-token"
SITE_ID = "your-site-id"
LIST_ID = "your-list-id"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

updates = [
    {"id": "1", "Status": "Closed"},
    {"id": "2", "Status": "In Progress"}
]

def update_item(item_id, fields):
    url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/lists/{LIST_ID}/items/{item_id}/fields"
    response = requests.patch(url, headers=headers, json=fields)

    if response.status_code == 200:
        print(f"Updated item {item_id}")
    else:
        print(f"Failed {item_id}: {response.text}")

def process_updates():
    for item in updates:
        item_id = item.pop("id")
        update_item(item_id, item)

if __name__ == "__main__":
    process_updates()
