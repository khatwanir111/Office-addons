import os
import csv
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")

SCOPES = ["https://graph.microsoft.com/.default"]
OUTPUT_CSV = "user_licenses.csv"

def get_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET,
    )
    result = app.acquire_token_for_client(SCOPES)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))
    return result["access_token"]

def export_user_licenses():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://graph.microsoft.com/v1.0/users?$select=id,displayName,userPrincipalName,assignedLicenses"
    users = []

    while url:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        users.extend(data.get("value", []))
        url = data.get("@odata.nextLink")

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["displayName", "userPrincipalName", "skuIds"])
        for u in users:
            sku_ids = [lic.get("skuId") for lic in u.get("assignedLicenses", [])]
            writer.writerow([
                u.get("displayName"),
                u.get("userPrincipalName"),
                ";".join(map(str, sku_ids)),
            ])

    print(f"Exported {len(users)} users to {OUTPUT_CSV}")

if __name__ == "__main__":
    export_user_licenses()
