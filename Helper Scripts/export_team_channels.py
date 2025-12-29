import os, csv, requests, msal

TENANT_ID = os.getenv("M365_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET")
OUTPUT = "team_channels.csv"
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
    teams = requests.get(
        "https://graph.microsoft.com/v1.0/groups?$filter=resourceProvisioningOptions/Any(x:x eq 'Team')",
        headers=headers,
    ).json()["value"]

    rows = []
    for t in teams:
        ch = requests.get(
            f"https://graph.microsoft.com/v1.0/teams/{t['id']}/channels",
            headers=headers,
        )
        if ch.status_code == 200:
            for c in ch.json().get("value", []):
                rows.append({
                    "team": t.get("displayName"),
                    "channel": c.get("displayName"),
                })

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("Exported", len(rows), "channels")

if __name__ == "__main__":
    main()
