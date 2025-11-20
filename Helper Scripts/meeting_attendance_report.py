# meeting_attendance_report.py
import os, requests, csv, io
from helper_auth import get_token
from datetime import datetime, timedelta

WINDOW_DAYS = int(os.environ.get("WINDOW_DAYS", "7"))

def run():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    since = (datetime.utcnow() - timedelta(days=WINDOW_DAYS)).isoformat() + "Z"
    events_url = f"https://graph.microsoft.com/v1.0/me/events?$filter=start/dateTime ge '{since}'&$top=50"
    evs = requests.get(events_url, headers=headers)
    if not evs.ok:
        print("Failed to list events", evs.status_code, evs.text); return

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["meetingId","subject","participant","joinTime","leaveTime","duration"])

    for ev in evs.json().get("value", []):
        online_id = ev.get("onlineMeeting", {}).get("id")
        if not online_id:
            continue
        # attendance reports endpoint (may require permissions/availability)
        rep = requests.get(f"https://graph.microsoft.com/v1.0/me/onlineMeetings/{online_id}/attendanceReports", headers=headers)
        if not rep.ok:
            continue
        for ar in rep.json().get("value", []):
            # get attendance records
            recs = requests.get(f"https://graph.microsoft.com/v1.0/me/onlineMeetings/{online_id}/attendanceReports/{ar['id']}/attendanceRecords", headers=headers)
            if not recs.ok:
                continue
            for r in recs.json().get("value", []):
                writer.writerow([online_id, ev.get("subject"), r.get("identity", {}).get("user", {}).get("displayName"), r.get("joinDateTime"), r.get("leaveDateTime"), r.get("attendanceDuration")])

    csv_bytes = buf.getvalue().encode("utf-8")
    put = requests.put("https://graph.microsoft.com/v1.0/me/drive/root:/meeting_attendance.csv:/content",
                       headers={**headers, "Content-Type":"text/csv"}, data=csv_bytes)
    print("Saved meeting_attendance.csv:", put.status_code)

if __name__ == "__main__":
    run()
