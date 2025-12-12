import os
import csv
import requests
import msal
from datetime import datetime, timedelta, timezone

TENANT_ID = os.getenv("M365_TENANT_ID", "")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "")
OUTPUT = "expiring_passwords.csv"
DAYS_WINDOW = 14  # change as needed
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

def iso_to_dt(s):
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except:
        return None

def main():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://graph.microsoft.com/v1.0/users?$select=id,displayName,userPrincipalName,passwordPolicies,passwordProfile"
    users = []
    while url:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        users.extend(data.get("value", []))
        url = data.get("@odata.nextLink")

    cutoff = datetime.now(timezone.utc) + timedelta(days=DAYS_WINDOW)
    rows = []
    for u in users:
        # Note: Graph doesn't directly expose password expiry for each user unless using custom attributes or licensing.
        # Try to infer from passwordProfile.forceChangePasswordNextSignIn and lastPasswordChangeDateTime if present (best-effort).
        pp = u.get("passwordProfile") or {}
        last_change = pp.get("lastPasswordChangeDateTime") or u.get("lastPasswordChangeDateTime")
        dt = iso_to_dt(last_change) if last_change else None
        # naive assumption: if last change exists and policy uses 90 days expiry
        expiry = dt + timedelta(days=90) if dt else None
        if expiry and expiry <= cutoff:
            rows.append({
                "id": u.get("id"),
                "displayName": u.get("displayName"),
                "userPrincipalName": u.get("userPrincipalName"),
                "passwordExpiry": expiry.isoformat()
            })

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "displayName", "userPrincipalName", "passwordExpiry"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Written {len(rows)} users to {OUTPUT}")

if __name__ == "__main__":
    main()
