import os
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")

SCOPES = ["https://graph.microsoft.com/.default"]
GRAPH_APP_ID = "00000003-0000-0000-c000-000000000000"  # Microsoft Graph

def get_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET,
    )
    result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" not in result:
        raise RuntimeError(f"Token error: {result.get('error_description')}")
    return result["access_token"]

def list_sp_permissions():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Service principals that request Microsoft Graph permissions
    url = (
        "https://graph.microsoft.com/v1.0/servicePrincipals"
        f"?$filter=appId eq '{GRAPH_APP_ID}'"
        "&$expand=appRoleAssignedTo"
    )

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json().get("value", [])

    if not data:
        print("No Microsoft Graph service principal found.")
        return

    graph_sp = data[0]
    assignments = graph_sp.get("appRoleAssignedTo", [])

    print("=== App Permissions Against Microsoft Graph ===")
    for a in assignments:
        principal_display_name = a.get("principalDisplayName")
        app_role_id = a.get("appRoleId")
        print(f"{principal_display_name} -> AppRoleId: {app_role_id}")

if __name__ == "__main__":
    list_sp_permissions()
