import os, json, requests, msal

TENANT_ID = os.getenv("M365_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET")
USERS = ["user1@domain.com", "user2@domain.com"]
OUTPUT = "mailbox_settings.json"
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
    results = {}

    for u in USERS:
        r = requests.get(
            f"https://graph.microsoft.com/v1.0/users/{u}/mailboxSettings",
            headers=headers,
        )
        if r.status_code == 200:
            results[u] = r.json()
            print("Fetched mailbox settings for", u)
        else:
            print("Failed for", u, r.status_code)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("Written mailbox settings to", OUTPUT)

if __name__ == "__main__":
    main()
