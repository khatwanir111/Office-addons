import os, requests, msal

TENANT_ID = os.getenv("M365_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET")
THRESHOLD = 5
SCOPES = ["https://graph.microsoft.com/.default"]

def token():
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    ).acquire_token_for_client(SCOPES)["access_token"]

def main():
    headers = {"Authorization": f"Bearer {token()}"}
    apps = requests.get(
        "https://graph.microsoft.com/v1.0/applications?$select=displayName,requiredResourceAccess",
        headers=headers
    ).json()["value"]

    for a in apps:
        perms = sum(len(r.get("resourceAccess", [])) for r in a.get("requiredResourceAccess", []))
        if perms >= THRESHOLD:
            print(a.get("displayName"), "| permissions:", perms)

if __name__ == "__main__":
    main()
