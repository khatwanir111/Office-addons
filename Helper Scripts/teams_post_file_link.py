# teams_post_file_link.py
# Env: TEAM_ID, CHANNEL_ID
import os, requests
from helper_auth import get_token

def run():
    TEAM_ID = os.environ.get("TEAM_ID")
    CHANNEL_ID = os.environ.get("CHANNEL_ID")
    if not TEAM_ID or not CHANNEL_ID:
        print("Set TEAM_ID and CHANNEL_ID in env")
        return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # 1) Upload a test file to your personal OneDrive
    filename = "teams_shared_note.txt"
    content = b"This is an automated file for Teams channel."
    up = requests.put(f"https://graph.microsoft.com/v1.0/me/drive/root:/{filename}:/content", headers={**headers, "Content-Type":"text/plain"}, data=content)
    if not up.ok:
        print("Upload failed", up.status_code, up.text); return
    web_url = up.json().get("webUrl")

    # 2) Post message to channel with link
    msg_payload = {"body": {"content": f"Automated file uploaded: <a href=\"{web_url}\">{filename}</a>"}}
    post = requests.post(f"https://graph.microsoft.com/v1.0/teams/{TEAM_ID}/channels/{CHANNEL_ID}/messages", headers={**headers, "Content-Type":"application/json"}, json=msg_payload)
    print("Posted message status:", post.status_code, post.text)

if __name__ == "__main__":
    run()
