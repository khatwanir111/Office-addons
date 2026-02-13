import os, csv, requests, msal

TENANT_ID = os.getenv("M365_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET")
OUTPUT = "user_extension_attributes.csv"
SCOPES = ["https://graph.microsoft.com/.default"]

def token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    )
    return app.acquire_token_for_client(SCOPES)["access_token"]

def main():
    headers = {"Authorization": f"Bearer {token()}"}
    r = requests.get(
        "https://graph.microsoft.com/v1.0/users?$select=displayName,userPrincipalName,onPremisesExtensionAttributes",
        headers=headers
    )
    r.raise_for_status()

    rows = []
    for u in r.json().get("value", []):
        attrs = u.get("onPremisesExtensionAttributes") or {}
        rows.append({
            "upn": u.get("userPrincipalName"),
            "extensionAttribute1": attrs.get("extensionAttribute1"),
            "extensionAttribute2": attrs.get("extensionAttribute2")
        })

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("Exported", len(rows), "users")

if __name__ == "__main__":
    main()
