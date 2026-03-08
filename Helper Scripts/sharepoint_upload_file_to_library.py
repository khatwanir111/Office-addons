import requests

ACCESS_TOKEN = "your-access-token"
SITE_ID = "your-site-id"
FILE_PATH = "document.txt"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

def upload_file():
    filename = FILE_PATH.split("/")[-1]

    url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/drive/root:/{filename}:/content"

    with open(FILE_PATH, "rb") as f:
        response = requests.put(url, headers=headers, data=f)

    if response.status_code in (200, 201):
        print("File uploaded successfully")
    else:
        print("Upload failed:", response.text)

if __name__ == "__main__":
    upload_file()
