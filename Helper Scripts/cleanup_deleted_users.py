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

def main():
    headers = {"Authorization": f"Bearer {token()}"}
    url = "https://graph.microsoft.com/v1.0/directory/deletedItems/microsoft.graph.user"

    r = requests.get(url, headers=headers)
    r.raise_for_status()
    for u in r.json().get("value", []):
        d = requests.delete(
            f"https://graph.microsoft.com/v1.0/directory/deletedItems/{u['id']}",
            headers=headers,
        )
        d.raise_for_status()
        print("Permanently deleted:", u.get("displayName"))

if __name__ == "__main__":
    main()
