# teams_incoming_webhook_sender.py
# ENV: WEBHOOK_URL
import os, requests, json

def run():
    url = os.environ.get("WEBHOOK_URL")
    if not url:
        print("Set WEBHOOK_URL")
        return

    payload = {
        "@type": "MessageCard",
        "@context": "https://schema.org/extensions",
        "summary": "Automation notification",
        "themeColor": "0076D7",
        "title": "Automation Script Ran",
        "text": "This message was sent by a Python automation using an incoming webhook."
    }

    resp = requests.post(url, headers={"Content-Type":"application/json"}, data=json.dumps(payload))
    print("Webhook status:", resp.status_code, resp.text)

if __name__ == "__main__":
    run()
