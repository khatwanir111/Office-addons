import os, csv, requests, msal

TENANT_ID = os.getenv("M365_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET")
OUTPUT = "group_owners.csv"
SCOPES = ["https://graph.microsoft.com/.default"]

def token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    )
    return app.acquire_token_for_client(SCOPES)["access_token"]

def main():
    headers = {"Authorization": f"Bearer {token()}"}
    groups = requests.get("https://graph.microsoft.com/v1.0/groups", headers=headers).json()["value"]
    rows = []

    for g in groups:
        owners = requests.get(
            f"https://graph.microsoft.com/v1.0/groups/{g['id']}/owners",
            headers=headers
        ).json().get("value", [])
        for o in owners:
            rows.append({
                "group": g.get("displayName"),
                "owner": o.get("displayName"),
                "ownerUpn": o.get("userPrincipalName"),
            })

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("Exported", len(rows), "rows")

if __name__ == "__main__":
    main()
