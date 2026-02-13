import os, csv, requests, msal

TENANT_ID = os.getenv("M365_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET")
OUTPUT = "user_license_details.csv"
SCOPES = ["https://graph.microsoft.com/.default"]

def token():
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    ).acquire_token_for_client(SCOPES)["access_token"]

def main():
    headers = {"Authorization": f"Bearer {token()}"}
    users = requests.get(
        "https://graph.microsoft.com/v1.0/users?$select=id,userPrincipalName",
        headers=headers
    ).json()["value"]

    rows = []
    for u in users:
        r = requests.get(
            f"https://graph.microsoft.com/v1.0/users/{u['id']}/licenseDetails",
            headers=headers
        )
        if r.status_code == 200:
            for lic in r.json().get("value", []):
                rows.append({
                    "upn": u.get("userPrincipalName"),
                    "skuPartNumber": lic.get("skuPartNumber")
                })

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("Exported", len(rows), "license records")

if __name__ == "__main__":
    main()
