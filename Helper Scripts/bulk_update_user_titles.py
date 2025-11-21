# bulk_update_user_titles.py
# ENV: CSV_ONEDRIVE_PATH (optional, e.g. "/updates/titles.csv") or LOCAL_CSV (fallback)
import os, requests, io, csv
from helper_auth import get_token

def fetch_csv_from_onedrive(path):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"https://graph.microsoft.com/v1.0/me/drive/root:{path}:/content", headers=headers)
    return r.content.decode() if r.ok else None

def run():
    csv_path = os.environ.get("CSV_ONEDRIVE_PATH")
    local_csv = os.environ.get("LOCAL_CSV", "titles.csv")
    data = None
    if csv_path:
        data = fetch_csv_from_onedrive(csv_path)
    if not data and os.path.exists(local_csv):
        data = open(local_csv, "r", encoding="utf-8").read()
    if not data:
        print("No CSV found"); return

    reader = csv.DictReader(io.StringIO(data))
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}
    for row in reader:
        upn = row.get("userPrincipalName")
        title = row.get("jobTitle")
        if not upn or title is None:
            continue
        resp = requests.patch(f"https://graph.microsoft.com/v1.0/users/{upn}", headers=headers, json={"jobTitle": title})
        print(upn, resp.status_code)

if __name__ == "__main__":
    run()
