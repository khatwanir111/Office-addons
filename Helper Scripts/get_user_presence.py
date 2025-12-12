import os
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "")
USER_UPNS = ["user1@domain.com", "user2@domain.com"]
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

def main():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    for upn in USER_UPNS:
        r = requests.get(f"https://graph.microsoft.com/v1.0/users/{upn}/presence", headers=headers)
        if r.status_code == 200:
            p = r.json()
            print(upn, "| availability:", p.get("availability"), "| activity:", p.get("activity"))
        else:
            print(upn, "| failed to fetch presence:", r.status_code, r.text)

if __name__ == "__main__":
    main()
