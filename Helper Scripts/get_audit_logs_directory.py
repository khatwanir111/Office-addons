import os
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "")

# Requires AuditLog.Read.All
SCOPES = ["https://graph.microsoft.com/.default"]

def get_token():
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    ).acquire_token_for_client(SCOPES)["access_token"]

def get_logs(top=20):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://graph.microsoft.com/v1.0/auditLogs/directoryAudits?$top={top}"

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    logs = resp.json().get("value", [])

    for l in logs:
        print(
            l.get("activityDateTime"),
            "|",
            l.get("activityDisplayName"),
            "|",
            l.get("initiatedBy", {}).get("user", {}).get("userPrincipalName")
        )

if __name__ == "__main__":
    get_logs(20)
