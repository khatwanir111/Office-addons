import os
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")

# Requires audit/sign-in permissions, e.g. AuditLog.Read.All
SCOPES = ["https://graph.microsoft.com/.default"]

def get_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET,
    )
    result = app.acquire_token_for_client(SCOPES)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))
    return result["access_token"]

def get_signins(top=25):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ConsistencyLevel": "eventual",
    }
    url = f"https://graph.microsoft.com/v1.0/auditLogs/signIns?$top={top}"

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    signins = resp.json().get("value", [])

    for s in signins:
        user = s.get("userPrincipalName")
        time = s.get("createdDateTime")
        status = s.get("status", {}).get("errorCode")
        client_app = s.get("clientAppUsed")
        print(f"{time} | {user} | status={status} | app={client_app}")

if __name__ == "__main__":
    get_signins(25)
