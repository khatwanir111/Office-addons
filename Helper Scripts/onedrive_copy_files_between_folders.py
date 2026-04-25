import requests

ACCESS_TOKEN = "your-access-token"
SOURCE_FOLDER_ID = "source-folder-id"
TARGET_FOLDER_ID = "target-folder-id"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def get_files():
    url = f"https://graph.microsoft.com/v1.0/me/drive/items/{SOURCE_FOLDER_ID}/children"
    response = requests.get(url, headers=headers)
    return response.json().get("value", [])

def copy_file(file):
    url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file['id']}/copy"

    payload = {
        "parentReference": {"id": TARGET_FOLDER_ID},
        "name": file["name"]
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code in (202, 201):
        print(f"Copy initiated: {file['name']}")

if __name__ == "__main__":
    for f in get_files():
        if "file" in f:
            copy_file(f)
