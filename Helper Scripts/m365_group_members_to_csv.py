import os
import csv
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")

SCOPES = ["https://graph.microsoft.com/.default"]
GROUP_ID = "YOUR_GROUP_ID"
OUTPUT_CSV = "group_members.csv"

def get_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET,
    )
    result = app.acquire_token_for_client(SCOPES)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))
    return result["access_token"]

def export_group_members():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://graph.microsoft.com/v1.0/groups/{GROUP_ID}/members?$select=id,displayName,mail,userPrincipalName"
    members = []

    while url:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        members.extend(data.get("value", []))
        url = data.get("@odata.nextLink")

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "displayName", "mail", "userPrincipalName"])
        for m in members:
            writer.writerow([
                m.get("id"),
                m.get("displayName"),
                m.get("mail"),
                m.get("userPrincipalName"),
            ])

    print(f"Exported {len(members)} members to {OUTPUT_CSV}")

if __name__ == "__main__":
    export_group_members()
