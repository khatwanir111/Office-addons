# cleanup_expired_subscriptions.py
# ENV: GRACE_HOURS (optional, default 1)
import os, requests
from datetime import datetime, timezone, timedelta
from helper_auth import get_token

def run():
    grace = int(os.environ.get("GRACE_HOURS", "1"))
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}
    subs = requests.get("https://graph.microsoft.com/v1.0/subscriptions", headers=headers)
    if not subs.ok:
        print("Failed to list subscriptions", subs.status_code, subs.text); return
    now = datetime.now(timezone.utc)
    for s in subs.json().get("value", []):
        exp = s.get("expirationDateTime")
        if not exp: continue
        exp_dt = datetime.fromisoformat(exp.replace("Z","+00:00"))
        if exp_dt < now + timedelta(hours=-grace) or exp_dt <= now + timedelta(hours=grace):
            # delete subscription
            sid = s["id"]
            d = requests.delete(f"https://graph.microsoft.com/v1.0/subscriptions/{sid}", headers=headers)
            print("Deleted subscription", sid, "status", d.status_code)
    print("Cleanup done.")

if __name__ == "__main__":
    run()
