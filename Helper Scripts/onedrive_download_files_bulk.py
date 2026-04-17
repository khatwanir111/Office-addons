import requests
import os

ACCESS_TOKEN = "your-access-token"
DOWNLOAD_PATH = "downloads"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

def get_files():
    url = "https://graph.microsoft.com/v1.0/me/drive/root/children"
    response = requests.get(url, headers=headers)
    return response.json().get("value", [])

def download_file(file):
    if "file" not in file:
        return

    name = file["name"]
    download_url = file["@microsoft.graph.downloadUrl"]

    os.makedirs(DOWNLOAD_PATH, exist_ok=True)
    filepath = os.path.join(DOWNLOAD_PATH, name)

    content = requests.get(download_url).content
    with open(filepath, "wb") as f:
        f.write(content)

    print(f"Downloaded: {name}")

if __name__ == "__main__":
    files = get_files()
    for f in files:
        download_file(f)
