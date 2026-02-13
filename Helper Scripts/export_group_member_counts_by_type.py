import os, csv, requests, msal

TENANT_ID = os.getenv("M365_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET")
OUTPUT = "group_member_counts_by_type.csv"
SCOPES = ["https://graph.microsoft.com/.default"]

def token():
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    ).acquire_token_for_client(SCOPES)["access_token"]

def main():
    headers = {"Authorization": f"Bearer {token()}", "ConsistencyLevel": "eventual"}
    groups = requests.get(
        "https://graph.microsoft.com/v1.0/groups?$select=id,displayName,securityEnabled,groupTypes",
        headers=headers
    ).json()["value"]

    rows = []
    for g in groups:
        count = requests.get(
            f"https://graph.microsoft.com/v1.0/groups/{g['id']}/members/$count",
            headers=headers
        ).text
        rows.append({
            "group": g.get("displayName"),
            "type": "Security" if g.get("securityEnabled") else "Microsoft365",
            "memberCount": count
        })

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("Exported", len(rows), "groups")

if __name__ == "__main__":
    main()
