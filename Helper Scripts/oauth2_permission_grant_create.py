# oauth2_permission_grant_create.py
import os, requests, json
from helper_auth import get_token

def run():
    client_app_id = os.environ.get("CLIENT_APP_ID")
    resource_app_id = os.environ.get("RESOURCE_APP_ID")
    principal_id = os.environ.get("PRINCIPAL_ID")  # user or service principal object id
    if not (client_app_id and resource_app_id and principal_id):
        print("Set CLIENT_APP_ID, RESOURCE_APP_ID, PRINCIPAL_ID")
        return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    payload = {
        "clientId": client_app_id,
        "consentType": "AllPrincipals",
        "principalId": principal_id,
        "resourceId": resource_app_id,
        "scope": "user.read openid profile offline_access"
    }
    resp = requests.post("https://graph.microsoft.com/v1.0/oauth2PermissionGrants", headers=headers, json=payload)
    print(resp.status_code, resp.text)

if __name__ == "__main__":
    run()
