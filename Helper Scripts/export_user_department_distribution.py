import os, csv, requests, msal
from collections import Counter

TENANT_ID = os.getenv("M365_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET")
OUTPUT = "user_department_distribution.csv"
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
        "https://graph.microsoft.com/v1.0/users?$select=department",
        headers=headers
    )
    r.raise_for_status()

    counter = Counter()
    for u in r.json().get("value", []):
        counter[u.get("department") or "Unknown"] += 1

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["department", "count"])
        for dept, count in counter.items():
            writer.writerow([dept, count])

    print("Exported department distribution")

if __name__ == "__main__":
    main()
