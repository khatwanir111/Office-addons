# backup_sharepoint_doclib.py
import os, requests, zipfile, io
from helper_auth import get_token

def backup_site_doclib(site_id, drive_id=None):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # list items in drive (document library)
    drive_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive"
    if drive_id:
        drive_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}"
    items = requests.get(drive_url + "/root/children", headers=headers).json().get("value", [])

    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, mode="w") as zf:
        for it in items:
            if it.get("file"):
                name = it["name"]
                download = requests.get(f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{it['id']}/content", headers=headers)
                if download.ok:
                    zf.writestr(name, download.content)
                    print("Added to zip:", name)
                else:
                    print("Failed to download:", name)

    mem_zip.seek(0)
    # upload zip to OneDrive
    requests.put("https://graph.microsoft.com/v1.0/me/drive/root:/sharepoint_backup.zip:/content",
                 headers={**headers, "Content-Type": "application/zip"}, data=mem_zip.read())
    print("Backup uploaded to OneDrive.")

if __name__ == "__main__":
    # set SITE_ID env var or replace below
    site = os.environ.get("SITE_ID")
    if not site:
        print("Set SITE_ID environment variable to the SharePoint site id.")
    else:
        backup_site_doclib(site)
