# create_app_role_and_assign.py
# ENV: APP_OBJECT_ID (application object id), ROLE_NAME, PRINCIPAL_ID (user or service principal object id)
import os, requests, json
from helper_auth import get_token
from uuid import uuid4

def run():
    app_obj_id = os.environ.get("APP_OBJECT_ID")
    role_name = os.environ.get("ROLE_NAME", "AutoRole")
    principal_id = os.environ.get("PRINCIPAL_ID")
    if not (app_obj_id and principal_id):
        print("Set APP_OBJECT_ID and PRINCIPAL_ID"); return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    # create a new appRole on the application
    new_role = {
        "allowedMemberTypes": ["User"],
        "description": f"Auto-created role {role_name}",
        "displayName": role_name,
        "id": str(uuid4()),
        "isEnabled": True,
        "value": role_name.lower()
    }
    # patch application to add appRole
    app = requests.get(f"https://graph.microsoft.com/v1.0/applications/{app_obj_id}", headers=headers).json()
    current_roles = app.get("appRoles", [])
    current_roles.append(new_role)
    patch = requests.patch(f"https://graph.microsoft.com/v1.0/applications/{app_obj_id}", headers=headers, json={"appRoles": current_roles})
    if not patch.ok:
        print("Failed to add appRole:", patch.status_code, patch.text); return
    print("App role added. id:", new_role["id"])

    # find service principal for app
    sps = requests.get(f"https://graph.microsoft.com/v1.0/servicePrincipals?$filter=appId eq '{app.get('appId')}'", headers=headers).json().get("value", [])
    if not sps:
        print("Service principal not found; create it or wait"); return
    sp_id = sps[0]["id"]

    # assign the app role to the principal
    assign_payload = {
        "principalId": principal_id,
        "resourceId": sp_id,
        "appRoleId": new_role["id"]
    }
    resp = requests.post(f"https://graph.microsoft.com/v1.0/servicePrincipals/{sp_id}/appRoleAssignedTo", headers=headers, json=assign_payload)
    print("Role assignment status:", resp.status_code, resp.text)

if __name__ == "__main__":
    run()
