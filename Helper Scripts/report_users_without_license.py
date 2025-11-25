# report_users_without_license.py
# ENV: none
import os, requests, csv, io
from helper_auth import get_token

def run():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    url = "https://graph.microsoft.com/v1.0/users?$select=id,displayName,userPrincipalName,assignedLicenses&$top=50"
    all_users = []
    while url:
        r = requests.get(url, headers=headers)
        if not r.ok:
            print("Users fetch failed", r.status_code, r.text); return
        data = r.json()
        all_users.extend(data.get("value", []))
        url = data.get("@odata.nextLink")

    rows = []
    for u in all_users:
        if not u.get("assignedLicenses"):
            rows.append((u.get("displayName"), u.get("userPrincipalName"), u.get("id")))

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["displayName","userPrincipalName","id"])
    writer.writerows(rows)

    put = requests.put("https://graph.microsoft.com/v1.0/me/drive/root:/users_without_license.csv:/content",
                       headers={**headers, "Content-Type":"text/csv"}, data=buf.getvalue().encode("utf-8"))
    print("Saved users_without_license.csv:", put.status_code)

if __name__ == "__main__":
    run()
