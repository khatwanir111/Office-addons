import os, requests, msal

TENANT_ID = os.getenv("M365_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET")
SCOPES = ["https://graph.microsoft.com/.default"]

def token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET,
    )
    return app.acquire_token_for_client(SCOPES)["access_token"]

def count(endpoint):
    r = requests.get(endpoint, headers={"Authorization": f"Bearer {token()}"})
    r.raise_for_status()
    return len(r.json().get("value", []))

def main():
    users = count("https://graph.microsoft.com/v1.0/users?$top=999")
    groups = count("https://graph.microsoft.com/v1.0/groups?$top=999")
    teams = count("https://graph.microsoft.com/v1.0/groups?$filter=resourceProvisioningOptions/Any(x:x eq 'Team')")

    print("Directory activity summary")
    print("Users:", users)
    print("Groups:", groups)
    print("Teams:", teams)

if __name__ == "__main__":
    main()
