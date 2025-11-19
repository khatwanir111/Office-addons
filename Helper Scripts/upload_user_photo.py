# create_mail_template.py
import os, requests
from helper_auth import get_token

def run():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    draft = {
      "subject": "Status Update Template",
      "body": {"contentType": "HTML", "content": "<p>Hello team,<br/>This is the automated status template.</p>"},
      "toRecipients": []
    }
    resp = requests.post("https://graph.microsoft.com/v1.0/me/messages", headers=headers, json=draft)
    print("Draft create status:", resp.status_code, resp.text)
    if resp.ok:
        print("Draft id:", resp.json().get("id"))

if __name__ == "__main__":
    run()
