import requests

ACCESS_TOKEN = "your-access-token"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def get_files():
    url = "https://graph.microsoft.com/v1.0/me/drive/root/children"
    response = requests.get(url, headers=headers)
    return response.json().get("value", [])

def create_link(file_id):
    url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/createLink"

    payload = {"type": "view"}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        link = response.json().get("link", {}).get("webUrl")
        print(link)

if __name__ == "__main__":
    for f in get_files():
        if "file" in f:
            create_link(f["id"])
