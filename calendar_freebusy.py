# calendar_freebusy.py
import requests, json
from helper_auth import get_token
from datetime import datetime, timedelta

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

now = datetime.utcnow()
payload = {
  "schedules": [os.environ.get("USERNAME")],   # add other UPNs if you want
  "startTime": {"dateTime": now.isoformat(timespec='seconds'), "timeZone": "UTC"},
  "endTime": {"dateTime": (now + timedelta(hours=4)).isoformat(timespec='seconds'), "timeZone": "UTC"},
  "availabilityViewInterval": 30
}

resp = requests.post("https://graph.microsoft.com/v1.0/me/calendar/getSchedule", headers=headers, json=payload)
print(resp.status_code)
print(json.dumps(resp.json(), indent=2))
