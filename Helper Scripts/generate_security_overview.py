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

    policies = requests.get(
        "https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies",
        headers=headers,
    ).json().get("value", [])

    signins = requests.get(
        "https://graph.microsoft.com/v1.0/auditLogs/signIns?$top=20",
        headers={**headers, "ConsistencyLevel": "eventual"},
    ).json().get("value", [])

    print("Conditional access policies:", len(policies))
    print("Recent sign-ins:", len(signins))

if __name__ == "__main__":
    main()
