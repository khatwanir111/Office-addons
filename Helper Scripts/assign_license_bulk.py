import os
import csv
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")
SKU_ID = "YOUR_SKU_ID"  # skuId GUID to assign
INPUT_CSV = "users.csv"  # expects column userPrincipalName

SCOPES = ["https://graph.microsoft.com/.default"]

def get_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(SCOPES)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))
    return result["access_token"]

def assign_license(upn):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    url = f"https://graph.microsoft.com/v1.0/users/{upn}/assignLicense"
    payload = {"addLicenses": [{"skuId": SKU_ID}], "removeLicenses": []}
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code in (200, 202):
        print(f"Assigned license to {upn}")
    else:
        print(f"Failed for {upn}: {resp.status_code} {resp.text}")

def main():
    if not os.path.exists(INPUT_CSV):
        print(f"{INPUT_CSV} not found.")
        return
    with open(INPUT_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            upn = row.get("userPrincipalName") or row.get("upn")
            if upn:
                assign_license(upn.strip())

if __name__ == "__main__":
    main()
