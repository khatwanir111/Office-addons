import os
import json
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")

# Requires appropriate security permissions (e.g. SecurityEvents.Read.All)
SCOPES = ["https://graph.microsoft.com/.default"]
OUTPUT_JSON = "security_alerts.json"

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

def export_security_alerts(top=50):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://graph.microsoft.com/v1.0/security/alerts_v2?$top={top}"

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    alerts = data.get("value", [])

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(alerts, f, indent=2)

    print(f"Exported {len(alerts)} alerts to {OUTPUT_JSON}")
    for a in alerts[:10]:
        print(f"- {a.get('createdDateTime')} | {a.get('severity')} | {a.get('title')}")

if __name__ == "__main__":
    export_security_alerts(50)
