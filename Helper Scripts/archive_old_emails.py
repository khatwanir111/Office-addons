# archive_old_emails.py
import os, requests
from datetime import datetime, timedelta
from helper_auth import get_token

def run(days=30):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    # ensure folder exists
    create = requests.post("https://graph.microsoft.com/v1.0/me/mailFolders", headers=headers, json={"displayName":"AutomatedArchive"})
    if create.ok:
        folder_id = create.json()["id"]
    else:
        folders = requests.get("https://graph.microsoft.com/v1.0/me/mailFolders", headers=headers).json().get("value", [])
        folder_id = next((f["id"] for f in folders if f["displayName"]=="AutomatedArchive"), None)

    cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat() + "Z"
    q = f"https://graph.microsoft.com/v1.0/me/messages?$filter=receivedDateTime lt {cutoff}&$top=50"
    resp = requests.get(q, headers=headers)
    for m in resp.json().get("value", []):
        mid = m["id"]
        move_resp = requests.post(f"https://graph.microsoft.com/v1.0/me/messages/{mid}/move", headers=headers, json={"destinationId": folder_id})
        print("Moved", mid, move_resp.status_code)

if __name__ == "__main__":
    run(int(os.environ.get("ARCHIVE_AFTER_DAYS", "90")))
