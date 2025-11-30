import os
import json
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")

SCOPES = ["https://graph.microsoft.com/.default"]
USER_ID = "user@domain.com"
OUTPUT_JSON = "mailbox_rules.json"

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

def export_rules():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://graph.microsoft.com/v1.0/users/{USER_ID}/mailFolders/inbox/messageRules"

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    rules = resp.json().get("value", [])

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(rules, f, indent=2)

    print(f"Exported {len(rules)} rules to {OUTPUT_JSON}")
    for r in rules:
        print(f"- {r.get('displayName')} (Enabled={r.get('isEnabled')})")

if __name__ == "__main__":
    export_rules()
