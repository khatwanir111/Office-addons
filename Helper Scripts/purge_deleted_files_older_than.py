# purge_deleted_files_older_than.py
# ENV: DAYS_OLD (default 30)
import os, requests
from datetime import datetime, timezone, timedelta
from helper_auth import get_token

def run():
    days_old = int(os.environ.get("DAYS_OLD", "30"))
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_old)

    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Recycle bin items endpoint (may vary by tenant/Graph version)
    url = "https://graph.microsoft.com/v1.0/me/drive/recycleBin?$top=50"
    while url:
        r = requests.get(url, headers=headers)
        if not r.ok:
            print("Recycle bin fetch failed:", r.status_code, r.text)
            return
        data = r.json()
        for item in data.get("value", []):
            deleted = item.get("deleted", {}).get("stateChangeDateTime")
            if not deleted:
                continue
            deleted_dt = datetime.fromisoformat(deleted.replace("Z","+00:00"))
            if deleted_dt < cutoff:
                iid = item["id"]
                del_resp = requests.delete(f"https://graph.microsoft.com/v1.0/me/drive/recycleBin/items/{iid}", headers=headers)
                print("Purged:", item.get("name"), del_resp.status_code)
        url = data.get("@odata.nextLink")

    print("Purge completed for items older than", days_old, "days.")

if __name__ == "__main__":
    run()
