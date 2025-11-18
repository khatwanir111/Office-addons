# trigger_power_automate_flow_http.py
import os, requests, json
from helper_auth import get_token

def run():
    trigger_url = os.environ.get("FLOW_TRIGGER_URL")  # the HTTP POST URL of a flow
    if not trigger_url:
        print("Set FLOW_TRIGGER_URL in env")
        return

    payload = {"message": "Triggered by automated script", "timestamp": __import__("datetime").datetime.utcnow().isoformat()}
    resp = requests.post(trigger_url, json=payload)
    print("Trigger status:", resp.status_code, resp.text)

if __name__ == "__main__":
    run()
