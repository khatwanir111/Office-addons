import os, csv, requests, msal

TENANT_ID = os.getenv("M365_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET")
OUTPUT = "user_office_locations.csv"
SCOPES = ["https://graph.microsoft.com/.default"]

def token():
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    ).acquire_token_for_client(SCOPES)["access_token"]

def main():
    headers = {"Authorization": f"Bearer {token()}"}
    r = requests.get(
        "https://graph.microsoft.com/v1.0/users?$select=displayName,userPrincipalName,officeLocation",
        headers=headers
    )
    r.raise_for_status()

    rows = []
    for u in r.json().get("value", []):
        rows.append({
            "name": u.get("displayName"),
            "upn": u.get("userPrincipalName"),
            "officeLocation": u.get("officeLocation"),
        })

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("Exported", len(rows), "users")

if __name__ == "__main__":
    main()
