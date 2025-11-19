# schema_extension_create_and_use.py
import os, requests, json
from helper_auth import get_token

def run():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    ext_id = f"extAuto{os.getpid()}"
    create_payload = {
      "id": ext_id,
      "description": "Auto schema extension",
      "targetTypes": ["User"],
      "properties": [{"name":"devFlag","type":"Boolean"}]
    }
    # create extension
    r = requests.post("https://graph.microsoft.com/v1.0/schemaExtensions", headers=headers, json=create_payload)
    if not r.ok:
        print("Create extension failed (might already exist):", r.status_code, r.text)
    else:
        print("Created schema extension:", r.json().get("id"))

    # apply to current user (may need to wait for extension availability)
    me = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers).json()
    upn = me.get("userPrincipalName")
    if not upn:
        print("Could not get current user"); return

    update_payload = {f"{ext_id}_devFlag": True}
    upd = requests.patch(f"https://graph.microsoft.com/v1.0/users/{upn}", headers=headers, json=update_payload)
    print("Apply extension status:", upd.status_code, upd.text)

if __name__ == "__main__":
    run()
