# teams_event_with_notes.py
import json
from datetime import datetime, timedelta
import requests
from helper_auth import get_token

def create_meeting_with_note(subject="Dev Automation Meeting"):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    start = (datetime.utcnow() + timedelta(hours=1)).isoformat() + "Z"
    end = (datetime.utcnow() + timedelta(hours=2)).isoformat() + "Z"
    payload = {
        "startDateTime": start,
        "endDateTime": end,
        "subject": subject,
        "participants": {"organizer": {"identity": {"user": {"id": None}}}}
    }

    r = requests.post("https://graph.microsoft.com/v1.0/me/onlineMeetings", headers=headers, json=payload)
    if not r.ok:
        print("Failed to create online meeting:", r.status_code, r.text)
        return

    meeting = r.json()
    join_url = meeting.get("joinWebUrl")
    note = f"Meeting created: {subject}\\nJoin URL: {join_url}\\nStarts: {start}"
    requests.put("https://graph.microsoft.com/v1.0/me/drive/root:/meeting_note.txt:/content",
                 headers={**headers, "Content-Type": "text/plain"}, data=note)
    print("Meeting created and note saved.")


if __name__ == "__main__":
    create_meeting_with_note()
