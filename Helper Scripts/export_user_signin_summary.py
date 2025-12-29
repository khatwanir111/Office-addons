import os, csv, requests, msal

TENANT_ID = os.getenv("M365_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET")
OUTPUT = "signin_summary.csv"
SCOPES = ["https://graph.microsoft.com/.default"]

def token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET,
    )
    return app.acquire_token_for_client(SCOPES)["access_token"]

def main():
    headers = {
        "Authorization": f"Bearer {token()}",
        "ConsistencyLevel": "eventual",
    }
    url = "https://graph.microsoft.com/v1.0/auditLogs/signIns?$top=100"
    rows = []

    r = requests.get(url, headers=headers)
    r.raise_for_status()

    for s in r.json().get("value", []):
        rows.append({
            "user": s.get("userPrincipalName"),
            "time": s.get("createdDateTime"),
            "app": s.get("appDisplayName"),
            "status": s.get("status", {}).get("errorCode"),
        })

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("Written", len(rows), "sign-in records")

if __name__ == "__main__":
    main()
