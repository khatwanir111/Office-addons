# teams_meeting_metadata_export.py
# ENV: DAYS (optional, default 7)
import os, requests, csv, io
from datetime import datetime, timedelta
from helper_auth import get_token

def run():
    days = int(os.environ.get("DAYS", "7"))
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    since = (datetime.utcnow() - timedelta(days=days)).isoformat() + "Z"
    url = f"https://graph.microsoft.com/v1.0/me/onlineMeetings?$filter=startDateTime ge {since}&$top=50"
    meetings = []
    r = requests.get(url, headers=headers)
    if not r.ok:
        print("Online meetings fetch failed:", r.status_code, r.text)
        return
    meetings.extend(r.json().get("value", []))

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["id","subject","start","end","joinUrl"])
    for m in meetings:
        writer.writerow([m.get("id"), m.get("subject"), m.get("startDateTime"), m.get("endDateTime"), m.get("joinWebUrl")])

    put = requests.put(
        "https://graph.microsoft.com/v1.0/me/drive/root:/online_meetings_metadata.csv:/content",
        headers={**headers, "Content-Type":"text/csv"},
        data=buf.getvalue().encode("utf-8")
    )
    print("Saved online_meetings_metadata.csv:", put.status_code)

if __name__ == "__main__":
    run()
