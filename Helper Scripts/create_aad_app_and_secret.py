# create_aad_app_and_secret.py
# Creates an AAD application, service principal, and client secret via Microsoft Graph
# Requires elevated permissions: Application.ReadWrite.All (admin consent)
import os
import json
import requests
from datetime import datetime, timedelta
from helper_auth import get_token

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# 1) Create application
app_payload = {
    "displayName": f"AutoApp-{int(datetime.utcnow().timestamp())}",
    "signInAudience": "AzureADMyOrg",  # single-tenant; change if needed
    "api": {
        "requestedAccessTokenVersion": 2
    }
}
resp = requests.post("https://graph.microsoft.com/v1.0/applications", headers=headers, json=app_payload)
if not resp.ok:
    print("Failed to create application:", resp.status_code, resp.text)
    raise SystemExit(1)

app_obj = resp.json()
app_id = app_obj["appId"]
app_object_id = app_obj["id"]
print("✅ Created application:", app_obj["displayName"], "| appId:", app_id, "| objectId:", app_object_id)

# 2) Create service principal for the app
sp_payload = {"appId": app_id}
sp_resp = requests.post("https://graph.microsoft.com/v1.0/servicePrincipals", headers=headers, json=sp_payload)
if not sp_resp.ok:
    # if service principal exists, Graph may return 400; try to GET it
    print("Service principal creation returned:", sp_resp.status_code)
    # attempt to find existing SP
    find_resp = requests.get(f"https://graph.microsoft.com/v1.0/servicePrincipals?$filter=appId eq '{app_id}'", headers=headers)
    if find_resp.ok and find_resp.json().get("value"):
        sp_obj = find_resp.json()["value"][0]
        sp_id = sp_obj["id"]
        print("Found existing service principal id:", sp_id)
    else:
        print("Failed to create/find service principal:", sp_resp.text)
        raise SystemExit(1)
else:
    sp_obj = sp_resp.json()
    sp_id = sp_obj["id"]
    print("✅ Created service principal id:", sp_id)

# 3) Add a client secret (password credential) to the application
secret_payload = {
    "passwordCredential": {
        "displayName": "auto-generated-secret",
        # expire in 90 days
        "endDateTime": (datetime.utcnow() + timedelta(days=90)).isoformat() + "Z",
        "startDateTime": datetime.utcnow().isoformat() + "Z"
    }
}
secret_resp = requests.post(f"https://graph.microsoft.com/v1.0/applications/{app_object_id}/addPassword", headers=headers, json=secret_payload)
if not secret_resp.ok:
    print("Failed to add password:", secret_resp.status_code, secret_resp.text)
    raise SystemExit(1)

secret_obj = secret_resp.json()
client_secret_value = secret_obj.get("secretText")  # secretText contains the secret value once
print("✅ Created client secret. Value (copy now, will not be shown again):")
print(client_secret_value)

# Summary output
print("\n--- SUMMARY ---")
print("Application (appId):", app_id)
print("Application objectId:", app_object_id)
print("Service Principal id:", sp_id)
print("Client secret (copy and store securely):", client_secret_value)
print("Secret expires at:", secret_obj.get("endDateTime"))
