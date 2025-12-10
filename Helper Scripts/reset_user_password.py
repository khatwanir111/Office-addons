import os
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "")

USER_ID = "USER_OBJECT_ID"
NEW_PASSWORD = "Pass@12345"
SCOPES = ["https://graph.microsoft.com/.default"]

def get_token():
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    ).acquire_token_for_client(SCOPES)["access_token"]

def reset_password():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    payload = {
        "passwordProfile": {
            "password": NEW_PASSWORD,
            "forceChangePasswordNextSignIn": True
        }
    }

    url = f"https://graph.microsoft.com/v1.0/users/{USER_ID}"
    resp = requests.patch(url, headers=headers, json=payload)
    resp.raise_for_status()
    print("Password reset successful.")

if __name__ == "__main__":
    reset_password()
