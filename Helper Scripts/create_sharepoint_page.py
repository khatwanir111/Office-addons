# create_sharepoint_page.py
import os, requests
from helper_auth import get_token

def run():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    # get root site id
    site = requests.get("https://graph.microsoft.com/v1.0/sites/root", headers=headers).json()
    site_id = site.get("id")

    page_payload = {
      "title": "Automated Dev Page",
      "pageLevel": "Published",
      "webParts": [
        {
          "displayName": "Text",
          "data": {
            "innerHtml": "<p>This page was created programmatically by a dev script.</p>"
          }
        }
      ]
    }

    # Graph page creation varies across tenants; try the sitePages endpoint
    resp = requests.post(f"https://graph.microsoft.com/v1.0/sites/{site_id}/pages", headers=headers, json=page_payload)
    if resp.ok:
        print("Page created:", resp.json().get("id"))
    else:
        print("Failed to create page:", resp.status_code, resp.text)

if __name__ == "__main__":
    run()
