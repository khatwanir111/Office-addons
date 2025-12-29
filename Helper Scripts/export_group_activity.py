import os, csv, requests, msal

TENANT_ID = os.getenv("M365_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET")
OUTPUT = "group_activity.csv"
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
    url = "https://graph.microsoft.com/v1.0/groups?$select=id,displayName,createdDateTime,resourceProvisioningOptions"
    rows = []

    while url:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        for g in data.get("value", []):
            rows.append({
                "id": g.get("id"),
                "displayName": g.get("displayName"),
                "createdDateTime": g.get("createdDateTime"),
                "isTeam": "Team" in (g.get("resourceProvisioningOptions") or []),
            })
        url = data.get("@odata.nextLink")

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("Exported", len(rows), "groups")

if __name__ == "__main__":
    main()
