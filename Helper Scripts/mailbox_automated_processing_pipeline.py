# mailbox_automated_processing_pipeline.py
import os, requests
from helper_auth import get_token

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# 1. Get unread messages with attachments
resp = requests.get("https://graph.microsoft.com/v1.0/me/messages?$filter=isRead eq false and hasAttachments eq true&$top=5", headers=headers)
msgs = resp.json().get("value", [])

for m in msgs:
    print("Processing:", m.get("subject"))
    # download attachments
    attachments = requests.get(f"https://graph.microsoft.com/v1.0/me/messages/{m['id']}/attachments", headers=headers).json().get("value", [])
    for a in attachments:
        if a.get("@odata.type") == "#microsoft.graph.fileAttachment":
            name = a["name"]
            content_bytes = __import__("base64").b64decode(a["contentBytes"])
            requests.put(f"https://graph.microsoft.com/v1.0/me/drive/root:/{name}:/content", headers={"Authorization": f"Bearer {token}"}, data=content_bytes)
    # mark message as read and categorize
    update = {"isRead": True, "categories": ["Processed-Auto"]}
    requests.patch(f"https://graph.microsoft.com/v1.0/me/messages/{m['id']}", headers=headers, json=update)

print("Pipeline run completed.")
