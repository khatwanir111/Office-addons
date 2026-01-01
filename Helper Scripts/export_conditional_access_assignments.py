import os, json, requests, msal

TENANT_ID = os.getenv("M365_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET")
OUTPUT = "conditional_access_assignments.json"
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
        "https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies",
        headers=headers
    )
    r.raise_for_status()

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(r.json().get("value", []), f, indent=2)

    print("Exported conditional access policies")

if __name__ == "__main__":
    main()
