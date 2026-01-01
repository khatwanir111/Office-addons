import os, requests, msal
from collections import Counter

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
    url = "https://graph.microsoft.com/v1.0/users?$select=country"
    counter = Counter()

    r = requests.get(url, headers=headers)
    r.raise_for_status()

    for u in r.json().get("value", []):
        counter[u.get("country") or "Unknown"] += 1

    for country, count in counter.items():
        print(country, ":", count)

if __name__ == "__main__":
    main()
