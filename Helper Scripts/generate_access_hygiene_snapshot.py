import os, requests, msal

TENANT_ID = os.getenv("M365_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET")
SCOPES = ["https://graph.microsoft.com/.default"]

def token():
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    ).acquire_token_for_client(SCOPES)["access_token"]

def main():
    headers = {"Authorization": f"Bearer {token()}"}

    disabled = requests.get(
        "https://graph.microsoft.com/v1.0/users?$filter=accountEnabled eq false",
        headers=headers
    ).json().get("value", [])

    devices = requests.get(
        "https://graph.microsoft.com/v1.0/devices?$select=approximateLastSignInDateTime",
        headers=headers
    ).json().get("value", [])

    stale = sum(1 for d in devices if not d.get("approximateLastSignInDateTime"))

    print("Disabled users:", len(disabled))
    print("Devices with no sign-in data:", stale)

if __name__ == "__main__":
    main()
