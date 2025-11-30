import os
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")

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

def print_service_health():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://graph.microsoft.com/v1.0/admin/serviceAnnouncement/issues"

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    issues = resp.json().get("value", [])

    if not issues:
        print("No active service issues.")
        return

    for i in issues:
        print(
            f"\n[{i.get('id')}] {i.get('title')}\n"
            f"Service: {', '.join(i.get('impactedServices', []))}\n"
            f"Status: {i.get('status')}\n"
        )

if __name__ == "__main__":
    print_service_health()
