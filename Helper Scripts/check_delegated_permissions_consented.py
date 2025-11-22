# check_delegated_permissions_consented.py
# ENV: APP_OBJECT_ID or APP_ID (appId)
import os, requests
from helper_auth import get_token

def run():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    app_id = os.environ.get("APP_ID")
    app_object_id = os.environ.get("APP_OBJECT_ID")

    if not (app_id or app_object_id):
        print("Set APP_ID or APP_OBJECT_ID"); return

    if not app_object_id:
        r = requests.get(f"https://graph.microsoft.com/v1.0/applications?$filter=appId eq '{app_id}'", headers=headers)
        if not r.ok or not r.json().get("value"):
            print("App not found"); return
        app_object_id = r.json()["value"][0]["id"]

    app = requests.get(f"https://graph.microsoft.com/v1.0/applications/{app_object_id}", headers=headers).json()
    delegated = app.get("requiredResourceAccess", [])
    # Check servicePrincipal permissions (grants)
    sp = requests.get(f"https://graph.microsoft.com/v1.0/servicePrincipals?$filter=appId eq '{app.get('appId')}'", headers=headers).json().get("value", [])
    if sp:
        sp_id = sp[0]["id"]
        grants = requests.get(f"https://graph.microsoft.com/v1.0/oauth2PermissionGrants?$filter=clientId eq '{sp_id}'", headers=headers).json().get("value", [])
    else:
        grants = []

    print("RequiredResourceAccess (excerpt):", delegated)
    print("Existing oauth2PermissionGrants (count):", len(grants))

if __name__ == "__main__":
    run()
