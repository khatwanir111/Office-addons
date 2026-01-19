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

def count(url, headers):
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return len(r.json().get("value", []))

def main():
    headers = {"Authorization": f"Bearer {token()}"}
    print("Users:", count("https://graph.microsoft.com/v1.0/users?$top=999", headers))
    print("Guests:", count("https://graph.microsoft.com/v1.0/users?$filter=userType eq 'Guest'", headers))
    print("Groups:", count("https://graph.microsoft.com/v1.0/groups?$top=999", headers))
    print("Teams:", count("https://graph.microsoft.com/v1.0/groups?$filter=resourceProvisioningOptions/Any(x:x eq 'Team')", headers))
    print("Devices:", count("https://graph.microsoft.com/v1.0/devices?$top=999", headers))
    print("Apps:", count("https://graph.microsoft.com/v1.0/applications?$top=999", headers))

if __name__ == "__main__":
    main()
