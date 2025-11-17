# provision_sharepoint_site.py
import requests
from helper_auth import get_token
import json

def create_communication_site(title="AutoCommSite", alias=None, description="Auto-created site"):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    if alias is None:
        alias = f"autosite{int(__import__('time').time())}"

    payload = {
        "displayName": title,
        "alias": alias,
        "description": description,
        "webTemplate": "SITEPAGEPUBLISHING#0"  # communication site template
    }

    r = requests.post("https://graph.microsoft.com/v1.0/sites/root/create", headers=headers, json=payload)
    # Graph's site creation path may differ across tenants; if that fails, print response for debugging
    if r.ok:
        print("Site creation queued/created:", r.json())
    else:
        print("Site creation failed:", r.status_code, r.text)


if __name__ == "__main__":
    create_communication_site()
