# upload_user_photo.py
import os, requests
from helper_auth import get_token

def run():
    upn = os.environ.get("TARGET_USER_UPN")
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"image/jpeg"}

    # tiny JPEG placeholder bytes (this is not a valid image, replace with real bytes if available)
    img_bytes = b"\xff\xd8\xff\xe0" + b"PROFILEIMAGE"  # placeholder
    if upn:
        url = f"https://graph.microsoft.com/v1.0/users/{upn}/photo/$value"
    else:
        url = "https://graph.microsoft.com/v1.0/me/photo/$value"
    resp = requests.put(url, headers=headers, data=img_bytes)
    print("Photo upload status:", resp.status_code, resp.text)

if __name__ == "__main__":
    run()
