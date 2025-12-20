import os, requests, msal

TENANT_ID = os.getenv("M365_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET")
USER_OBJECT_ID = "USER_OBJECT_ID"
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
    url = f"https://graph.microsoft.com/v1.0/users/{USER_OBJECT_ID}/memberOf"

    groups = []
    while url:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        groups.extend(data.get("value", []))
        url = data.get("@odata.nextLink")

    for g in groups:
        gid = g.get("id")
        d = requests.delete(
            f"https://graph.microsoft.com/v1.0/groups/{gid}/members/{USER_OBJECT_ID}/$ref",
            headers=headers,
        )
        if d.status_code in (204, 202):
            print("Removed from group:", g.get("displayName"))
        else:
            print("Failed:", g.get("displayName"), d.status_code)

if __name__ == "__main__":
    main()
