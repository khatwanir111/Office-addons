# export_user_photos_batch.py
# ENV: USER_UPNS (comma-separated list)
import os, requests
from helper_auth import get_token

def run():
    upns = [u.strip() for u in os.environ.get("USER_UPNS","").split(",") if u.strip()]
    if not upns:
        print("Set USER_UPNS"); return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    for upn in upns:
        r = requests.get(f"https://graph.microsoft.com/v1.0/users/{upn}/photo/$value", headers=headers)
        if r.ok:
            name = upn.replace("@","_") + ".jpg"
            put = requests.put(f"https://graph.microsoft.com/v1.0/me/drive/root:/{name}:/content",
                               headers={**headers, "Content-Type":"image/jpeg"}, data=r.content)
            print("Saved", name, put.status_code)
        else:
            print("No photo for", upn, r.status_code)

if __name__ == "__main__":
    run()
