# export_site_template_files.py
# ENV: SITE_ID (optional; uses root if missing)
import os, json, requests
from helper_auth import get_token

def run():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    site_id = os.environ.get("SITE_ID")

    if site_id:
        url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root/children"
    else:
        url = "https://graph.microsoft.com/v1.0/me/drive/root/children"

    items = []
    r = requests.get(url, headers=headers)
    if r.ok:
        for it in r.json().get("value", []):
            items.append({"name": it.get("name"), "id": it.get("id"), "webUrl": it.get("webUrl")})

    manifest = {"exportedAt": __import__("datetime").datetime.utcnow().isoformat() + "Z", "items": items}
    put = requests.put("https://graph.microsoft.com/v1.0/me/drive/root:/site_export_manifest.json:/content",
                       headers={**headers, "Content-Type": "application/json"}, data=json.dumps(manifest).encode("utf-8"))
    print("Saved manifest:", put.status_code)

if __name__ == "__main__":
    run()
