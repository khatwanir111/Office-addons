# set_user_preferences.py
# ENV: PREFERRED_LANG (e.g. "en-US"), TIMEZONE (e.g. "India Standard Time")
import os, requests
from helper_auth import get_token

def run():
    lang = os.environ.get("PREFERRED_LANG", "en-US")
    tz = os.environ.get("TIMEZONE", "UTC")

    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    payload = {
        "language": {"locale": lang, "displayName": lang},
        "timeZone": tz,
        "workingHours": {
            "daysOfWeek": ["monday","tuesday","wednesday","thursday","friday"],
            "startTime": "09:00:00.0000000",
            "endTime": "18:00:00.0000000",
            "timeZone": {"name": tz}
        }
    }
    resp = requests.patch("https://graph.microsoft.com/v1.0/me/mailboxSettings", headers=headers, json=payload)
    print("Update mailbox settings status:", resp.status_code, resp.text)

if __name__ == "__main__":
    run()
