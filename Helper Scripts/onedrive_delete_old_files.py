import requests
from datetime import datetime, timedelta

ACCESS_TOKEN = "your-access-token"
DAYS_OLD = 30

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

def get_files():
    url = "https://graph.microsoft.com/v1.0/me/drive/root/children"
    response = requests.get(url, headers=headers)
    return response.json().get("value", [])

def delete_file(file_id):
    url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}"
    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        print("Deleted:", file_id)

def process_files():
    threshold = datetime.utcnow() - timedelta(days=DAYS_OLD)

    for file in get_files():
        last_modified = file.get("lastModifiedDateTime")
        if last_modified:
            file_time = datetime.fromisoformat(last_modified.replace("Z", ""))
            if file_time < threshold:
                delete_file(file["id"])

if __name__ == "__main__":
    process_files()
