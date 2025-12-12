import os
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "")
USER_UPN = "user@domain.com"
SCOPES = ["https://graph.microsoft.com/.default"]

def get_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    )
    res = app.acquire_token_for_client(SCOPES)
    if "access_token" not in res:
        raise SystemExit(res.get("error_description"))
    return res["access_token"]

def sku_map(token):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get("https://graph.microsoft.com/v1.0/subscribedSkus", headers=headers)
    r.raise_for_status()
    return {s["skuId"]: s.get("skuPartNumber") for s in r.json().get("value", [])}

def main():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"https://graph.microsoft.com/v1.0/users/{USER_UPN}?$select=id,displayName,assignedLicenses", headers=headers)
    r.raise_for_status()
    user = r.json()
    mapping = sku_map(token)
    sku_names = [mapping.get(lic.get("skuId"), str(lic.get("skuId"))) for lic in user.get("assignedLicenses", [])]
    print("User:", user.get("displayName"), "|", user.get("userPrincipalName"))
    print("Assigned SKUs:", ", ".join(sku_names) if sku_names else "None")

if __name__ == "__main__":
    main()
