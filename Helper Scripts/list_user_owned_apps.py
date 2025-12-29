import os, requests, msal

TENANT_ID = os.getenv("M365_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET")
USER_ID = "user@domain.com"
SCOPES = ["https://graph.microsoft.com/.default"]

def token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET,
    )
    return app.acquire_token_for_client(SCOPES)["access_token"]

def main():
    headers = {"Authorization": f"Bearer {token()}"}
    url = f"https://graph.microsoft.com/v1.0/users/{USER_ID}/ownedObjects"

    r = requests.get(url, headers=headers)
    r.raise_for_status()

    for o in r.json().get("value", []):
        if o.get("@odata.type") == "#microsoft.graph.application":
            print(o.get("displayName"), "|", o.get("appId"))

if __name__ == "__main__":
    main()
