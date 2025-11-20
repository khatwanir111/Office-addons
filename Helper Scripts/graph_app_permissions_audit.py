# graph_app_permissions_audit.py
import os, requests, json
from helper_auth import get_token

def run():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    grants = requests.get("https://graph.microsoft.com/v1.0/oauth2PermissionGrants", headers=headers)
    ar = requests.get("https://graph.microsoft.com/v1.0/servicePrincipals?$expand=appRoleAssignedTo", headers=headers)
    out = {"grants": grants.json() if grants.ok else grants.text, "servicePrincipals": ar.json() if ar.ok else ar.text}
    # Save results to OneDrive
    put = requests.put("https://graph.microsoft.com/v1.0/me/drive/root:/app_permissions_audit.json:/content",
                       headers={**headers, "Content-Type":"application/json"}, data=json.dumps(out).encode("utf-8"))
    print("Saved audit:", put.status_code)

if __name__ == "__main__":
    run()
