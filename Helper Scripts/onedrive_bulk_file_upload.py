import requests
import os

ACCESS_TOKEN = "your-access-token"
LOCAL_FOLDER = "upload_files"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

def upload_file(filepath):
    filename = os.path.basename(filepath)

    url = f"https://graph.microsoft.com/v1.0/me/drive/root:/{filename}:/content"

    with open(filepath, "rb") as f:
        response = requests.put(url, headers=headers, data=f)

    if response.status_code in (200, 201):
        print(f"{filename} uploaded successfully")
    else:
        print(f"Upload failed for {filename}")

def upload_all():
    for file in os.listdir(LOCAL_FOLDER):
        full_path = os.path.join(LOCAL_FOLDER, file)
        if os.path.isfile(full_path):
            upload_file(full_path)

if __name__ == "__main__":
    upload_all()
