# create_group_calendar_event.py
# ENV: GROUP_ID
import os, requests
from datetime import datetime, timedelta
from helper_auth import get_token

def run():
    group_id = os.environ.get("GROUP_ID")
    if not group_id:
        print("Set GROUP_ID in env")
        return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    start = datetime.utcnow()
    end = start + timedelta(hours=1)
    payload = {
        "subject": "Automated Group Event",
        "body": {"contentType": "HTML", "content": "This event was created by automation."},
        "start": {"dateTime": start.isoformat() + "Z", "timeZone": "UTC"},
        "end": {"dateTime": end.isoformat() + "Z", "timeZone": "UTC"},
        "location": {"displayName": "Virtual"},
        "attendees": []
    }

    resp = requests.post(f"https://graph.microsoft.com/v1.0/groups/{group_id}/events", headers=headers, json=payload)
    if resp.ok:
        print("Created group event:", resp.json().get("id"))
    else:
        print("Failed:", resp.status_code, resp.text)

if __name__ == "__main__":
    run()
