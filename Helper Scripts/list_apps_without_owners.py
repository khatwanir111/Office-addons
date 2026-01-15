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
    apps = requests.get(
        "https://graph.microsoft.com/v1.0/applications?$select=id,displayName",
        headers=headers
    ).json()["value"]

    for a in apps:
        owners = requests.get(
            f"https://graph.microsoft.com/v1.0/applications/{a['id']}/owners",
            headers=headers
        )
        if owners.status_code == 200 and not owners.json().get("value"):
            print(a.get("displayName"))

if __name__ == "__main__":
    main()
