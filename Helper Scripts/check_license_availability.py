import os, requests, msal

TENANT_ID = os.getenv("M365_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET")
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
    r = requests.get("https://graph.microsoft.com/v1.0/subscribedSkus", headers=headers)
    r.raise_for_status()

    for sku in r.json().get("value", []):
        total = sku.get("prepaidUnits", {}).get("enabled", 0)
        used = sku.get("consumedUnits", 0)
        print(sku.get("skuPartNumber"), "| total:", total, "| used:", used)

if __name__ == "__main__":
    main()
