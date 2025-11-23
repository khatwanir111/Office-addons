# create_recurring_calendar_event.py
# ENV: ATTENDEE_UPNS (comma-separated)
import os, requests
from datetime import datetime, timedelta
from helper_auth import get_token

def run():
    attendee_upns = [u.strip() for u in os.environ.get("ATTENDEE_UPNS", "").split(",") if u.strip()]
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    start = (datetime.utcnow() + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
    end = start + timedelta(hours=1)

    attendees = [{"emailAddress":{"address":u},"type":"required"} for u in attendee_upns]

    event = {
        "subject": "Automated Daily Standup",
        "body": {"contentType":"Text","content":"Daily automated standup."},
        "start": {"dateTime": start.isoformat()+"Z", "timeZone":"UTC"},
        "end": {"dateTime": end.isoformat()+"Z", "timeZone":"UTC"},
        "recurrence": {
            "pattern": {"type":"daily","interval":1},
            "range": {"type":"noEnd","startDate": start.date().isoformat()}
        },
        "attendees": attendees,
        "reminderMinutesBeforeStart": 15
    }

    r = requests.post("https://graph.microsoft.com/v1.0/me/events", headers=headers, json=event)
    print("Create recurring event:", r.status_code, r.text)

if __name__ == "__main__":
    run()
