# sharepoint_set_folder_permissions.py
import os, requests
from helper_auth import get_token

def run():
    site_resp = requests.get("https://graph.microsoft.com/v1.0/sites/root", headers={"Authorization": f"Bearer {get_token()}"})
    if not site_resp.ok:
        print("Site fetch failed"); return
    site_id = site_resp.json()["id"]

    # path to folder in site drive (e.g., /Shared Documents/Automations)
    folder_path = os.environ.get("FOLDER_PATH", "/Shared Documents/Automations")
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    # get folder item
    item = requests.get(f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:{folder_path}", headers=headers)
    if not item.ok:
        print("Folder not found", item.status_code, item.text); return
    item_id = item.json()["id"]

    # break inheritance: Graph may not have direct breakInheritance; demo adding permission role assignment to a principal
    principal_id = os.environ.get("PRINCIPAL_ID")  # user or group id
    role = "write"  # or 'read'
    if not principal_id:
        print("Set PRINCIPAL_ID in env to assign permissions"); return

    payload = {
      "grantee": {"@odata.id": f"https://graph.microsoft.com/v1.0/directoryObjects/{principal_id}"},
      "roles": [role]
    }
    # Use driveItem invite to grant access (simpler)
    invite_payload = {"requireSignIn": True, "roles": [role], "recipients": [{"objectId": principal_id}], "sendInvitation": False}
    invite_resp = requests.post(f"https://graph.microsoft.com/v1.0/me/drive/items/{item_id}/invite", headers=headers, json=invite_payload)
    print("Permission grant status:", invite_resp.status_code, invite_resp.text)

if __name__ == "__main__":
    run()
