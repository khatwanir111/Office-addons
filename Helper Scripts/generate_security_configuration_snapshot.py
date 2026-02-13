import os, requests, msal

TENANT_ID = os.getenv("M365_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET")
SCOPES = ["https://graph.microsoft.com/.default"]

def token():
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    ).acquire_token_for_client(SCOPES)["access_token"]

def count(url, headers):
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return len(r.json().get("value", []))

def main():
    headers = {"Authorization": f"Bearer {token()}"}
    policies = count("https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies", headers)
    risky = count("https://graph.microsoft.com/v1.0/identityProtection/riskyUsers", headers)
    dynamic = count("https://graph.microsoft.com/v1.0/groups?$filter=membershipRule ne null", headers)

    print("Conditional Access Policies:", policies)
    print("Risky Users:", risky)
    print("Dynamic Groups:", dynamic)

if __name__ == "__main__":
    main()
