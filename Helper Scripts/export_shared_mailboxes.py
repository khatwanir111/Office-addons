import os, csv, requests, msal

TENANT_ID = os.getenv("M365_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET")
OUTPUT = "shared_mailboxes.csv"
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
    url = "https://graph.microsoft.com/v1.0/users?$filter=mailboxSettings/automaticRepliesSetting ne null"
    rows = []

    r = requests.get(url, headers=headers)
    r.raise_for_status()
    for u in r.json().get("value", []):
        rows.append({
            "displayName": u.get("displayName"),
            "mail": u.get("mail"),
        })

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} entries")

if __name__ == "__main__":
    main()
