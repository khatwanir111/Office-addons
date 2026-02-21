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

def main():
    headers = {"Authorization": f"Bearer {token()}"}

    devices = requests.get(
        "https://graph.microsoft.com/v1.0/devices?$select=isCompliant",
        headers=headers
    ).json().get("value", [])

    users = requests.get(
        "https://graph.microsoft.com/v1.0/users?$select=accountEnabled",
        headers=headers
    ).json().get("value", [])

    risky = requests.get(
        "https://graph.microsoft.com/v1.0/identityProtection/riskyUsers",
        headers=headers
    ).json().get("value", [])

    compliant = sum(1 for d in devices if d.get("isCompliant"))
    disabled = sum(1 for u in users if not u.get("accountEnabled"))

    print("Compliant devices:", compliant)
    print("Disabled accounts:", disabled)
    print("Risky users:", len(risky))

if __name__ == "__main__":
    main()
