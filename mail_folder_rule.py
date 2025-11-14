# mail_folder_rule.py
import requests, json
from helper_auth import get_token

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Create a folder first
create_folder = requests.post("https://graph.microsoft.com/v1.0/me/mailFolders", headers=headers, json={"displayName":"AutomatedArchive"})
if create_folder.ok:
    folder_id = create_folder.json()["id"]
else:
    # try to find existing
    all_folders = requests.get("https://graph.microsoft.com/v1.0/me/mailFolders", headers=headers).json().get("value", [])
    folder_id = next((f["id"] for f in all_folders if f["displayName"]=="AutomatedArchive"), None)

# Create inbox rule to move mails from a specific sender to this folder
rule_payload = {
    "displayName": "MoveFromExample",
    "sequence": 1,
    "conditions": {"senderContains": ["example@example.com"]},
    "actions": {"moveToFolder": folder_id},
    "isEnabled": True
}

resp = requests.post("https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules", headers=headers, json=rule_payload)
print(resp.status_code, resp.text)
