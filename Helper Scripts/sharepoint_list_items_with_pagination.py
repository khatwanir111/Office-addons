import requests

ACCESS_TOKEN = "your-access-token"
SITE_ID = "your-site-id"
LIST_ID = "your-list-id"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

def fetch_items():
    url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/lists/{LIST_ID}/items"
    all_items = []

    while url:
        response = requests.get(url, headers=headers)
        data = response.json()

        for item in data.get("value", []):
            fields = item.get("fields", {})
            all_items.append(fields)

        url = data.get("@odata.nextLink")

    return all_items

if __name__ == "__main__":
    items = fetch_items()
    for i, item in enumerate(items, 1):
        print(f"{i}: {item}")
