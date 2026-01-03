import os, csv, requests, msal

TENANT_ID = os.getenv("M365_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET")
OUTPUT = "signin_failures.csv"
SCOPES = ["https://graph.microsoft.com/.default"]

def token():
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    ).acquire_token_for_client(SCOPES)["access_token"]

def main():
    headers = {
        "Authorization": f"Bearer {token()}",
        "ConsistencyLevel": "eventual"
    }
    r = requests.get(
        "https://graph.microsoft.com/v1.0/auditLogs/signIns?$filter=status/errorCode ne 0&$top=50",
        headers=headers
    )
    r.raise_for_status()

    rows = []
    for s in r.json().get("value", []):
        rows.append({
            "user": s.get("userPrincipalName"),
            "time": s.get("createdDateTime"),
            "app": s.get("appDisplayName"),
            "errorCode": s.get("status", {}).get("errorCode"),
        })

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("Exported", len(rows), "failed sign-ins")

if __name__ == "__main__":
    main()
