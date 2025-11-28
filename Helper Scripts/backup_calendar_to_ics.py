# backup_calendar_to_ics.py
# ENV: DAYS_AHEAD (default 7)
import os, requests
from datetime import datetime, timedelta, timezone
from helper_auth import get_token

def format_dt(dt_str):
    # dt_str is ISO from Graph; return ICS format (UTC)
    dt = datetime.fromisoformat(dt_str.replace("Z","+00:00"))
    return dt.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

def run():
    days = int(os.environ.get("DAYS_AHEAD", "7"))
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    start = datetime.utcnow().isoformat() + "Z"
    end = (datetime.utcnow() + timedelta(days=days)).isoformat() + "Z"
    url = f"https://graph.microsoft.com/v1.0/me/calendarview?startdatetime={start}&enddatetime={end}&$top=100"
    resp = requests.get(url, headers=headers)
    if not resp.ok:
        print("Calendar fetch failed:", resp.status_code, resp.text)
        return
    events = resp.json().get("value", [])

    ics_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Auto M365 Backup//EN"
    ]

    for e in events:
        uid = e.get("id")
        dt_start = format_dt(e.get("start", {}).get("dateTime"))
        dt_end = format_dt(e.get("end", {}).get("dateTime"))
        subject = e.get("subject", "").replace("\n"," ")
        ics_lines.extend([
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTART:{dt_start}",
            f"DTEND:{dt_end}",
            f"SUMMARY:{subject}",
            "END:VEVENT"
        ])

    ics_lines.append("END:VCALENDAR")
    ics_data = "\r\n".join(ics_lines).encode("utf-8")

    put = requests.put(
        "https://graph.microsoft.com/v1.0/me/drive/root:/calendar_backup.ics:/content",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "text/calendar"},
        data=ics_data
    )
    print("Saved calendar_backup.ics:", put.status_code)

if __name__ == "__main__":
    run()
