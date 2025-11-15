# aad_app_role_assignment.py
import os, requests, json
from helper_auth import get_token

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Provide target service principal and principal (user/group) IDs in env
SERVICE_PRINCIPAL_ID = os.environ.get("SP_ID")
PRINCIPAL_ID = os.environ.get("PRINCIPAL_ID")  # user or group id
APP_ROLE_ID = os.environ.get("APP_ROLE_ID")    # role id defined on app

if not SERVICE_PRINCIPAL_ID or not PRINCIPAL_ID or not APP_ROLE_ID:
    print("Set SP_ID, PRINCIPAL_ID, and APP_ROLE_ID in env.")
    exit(0)

payload = {
  "principalId": PRINCIPAL_ID,
  "resourceId": SERVICE_PRINCIPAL_ID,
  "appRoleId": APP_ROLE_ID
}
resp = requests.post("https://graph.microsoft.com/v1.0/servicePrincipals/{}/appRoleAssignedTo".format(SERVICE_PRINCIPAL_ID), headers=headers, json=payload)
print(resp.status_code, resp.text)
