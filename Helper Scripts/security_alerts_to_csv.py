# security_alerts_to_csv.py
# ENV: none (needs SecurityEvents.Read.All or similar)
import os, requests, csv, io
from helper_auth import get_token

def run():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    url = "https://graph.microsoft.com/v1.0/security/alerts?$top=50"
    alerts = []
    while url:
        r = requests.get(url, headers=headers)
        if not r.ok:
            print("Alert fetch failed:", r.status_code, r.text)
            break
        data = r.json()
        alerts.extend(data.get("value", []))
        url = data.get("@odata.nextLink")

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["id","title","severity","status","category"])
    for a in alerts:
        writer.writerow([a.get("id"), a.get("title"), a.get("severity"), a.get("status"), a.get("category")])

    put = requests.put(
        "https://graph.microsoft.com/v1.0/me/drive/root:/security_alerts.csv:/content",
        headers={**headers, "Content-Type":"text/csv"},
        data=buf.getvalue().encode("utf-8")
    )
    print("Saved security_alerts.csv:", put.status_code)

if __name__ == "__main__":
    run()
