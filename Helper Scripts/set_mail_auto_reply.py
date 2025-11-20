# set_mail_auto_reply.py
import os, requests
from helper_auth import get_token
from datetime import datetime, timedelta

DAYS = int(os.environ.get("OOF_DAYS", "3"))

def run():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    end = (datetime.utcnow() + timedelta(days=DAYS)).isoformat() + "Z"
    payload = {
      "automaticRepliesSetting": {
        "status": "scheduled",
        "internalReplyMessage": "<p>I'm currently in focus time. I'll reply later.</p>",
        "externalReplyMessage": "I'm away and will respond soon.",
        "scheduledStartDateTime": {"dateTime": datetime.utcnow().isoformat(), "timeZone":"UTC"},
        "scheduledEndDateTime": {"dateTime": end, "timeZone":"UTC"},
        "externalAudience": "all"
      }
    }
    resp = requests.patch("https://graph.microsoft.com/v1.0/me/mailboxSettings", headers=headers, json=payload)
    print("Set auto-reply status:", resp.status_code, resp.text)

if __name__ == "__main__":
    run()
