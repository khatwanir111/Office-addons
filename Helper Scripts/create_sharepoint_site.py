# create_sharepoint_site.py
# ENV: SITE_DISPLAY_NAME, SITE_ALIAS, SITE_TYPE (optional: 'communication' or 'team', default 'communication')
import os, requests
from helper_auth import get_token

def run():
    name = os.environ.get("SITE_DISPLAY_NAME")
    alias = os.environ.get("SITE_ALIAS")
    site_type = os.environ.get("SITE_TYPE", "communication")
    if not (name and alias):
        print("Set SITE_DISPLAY_NAME and SITE_ALIAS"); return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    payload = {
        "displayName": name,
        "url": f"https://{os.environ.get('TENANT_DOMAIN','example.sharepoint.com')}/sites/{alias}",
        "description": "Created by automation",
        "siteCollection": {"hostName": os.environ.get("TENANT_DOMAIN","example.sharepoint.com")}
    }
    # Graph special endpoints: use /sites/create? use /sites? Create a site via /sites? Alternatively use /groups to create team site.
    if site_type == "team":
        # Create Microsoft 365 group (team-enabled)
        gpayload = {
            "displayName": name,
            "mailEnabled": True,
            "mailNickname": alias,
            "securityEnabled": False,
            "groupTypes": ["Unified"]
        }
        g = requests.post("https://graph.microsoft.com/v1.0/groups", headers=headers, json=gpayload)
        print("Group create status:", g.status_code, g.text)
    else:
        # Create communication site via SharePoint REST is usual; Graph site creation limited — attempt site creation via Graph (may require specific tenant config)
        r = requests.post("https://graph.microsoft.com/v1.0/sites/root/sites", headers=headers, json={"displayName": name, "siteCollection":"", "webTemplate":"SITEPAGEPUBLISHING#0"})
        print("Site create attempt:", r.status_code, r.text)

if __name__ == "__main__":
    run()
