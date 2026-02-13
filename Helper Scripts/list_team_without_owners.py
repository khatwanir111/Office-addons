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
    teams = requests.get(
        "https://graph.microsoft.com/v1.0/groups?$filter=resourceProvisioningOptions/Any(x:x eq 'Team')",
        headers=headers
    ).json()["value"]

    for t in teams:
        owners = requests.get(
            f"https://graph.microsoft.com/v1.0/groups/{t['id']}/owners",
            headers=headers
        ).json().get("value", [])
        if not owners:
            print(t.get("displayName"))

if __name__ == "__main__":
    main()
