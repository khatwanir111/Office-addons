import os, csv, requests, msal

TENANT_ID = os.getenv("M365_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET")
OUTPUT = "service_principals.csv"
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
    url = "https://graph.microsoft.com/v1.0/servicePrincipals"
    rows = []

    while url:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        for sp in data.get("value", []):
            rows.append({
                "displayName": sp.get("displayName"),
                "appId": sp.get("appId"),
                "id": sp.get("id"),
            })
        url = data.get("@odata.nextLink")

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Exported {len(rows)} service principals")

if __name__ == "__main__":
    main()
