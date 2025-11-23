# auto_reply_to_subjects.py
# ENV: SUBJECT_KEYWORD (e.g. "Support"), REPLY_BODY (optional)
import os, requests
from helper_auth import get_token

def run():
    keyword = os.environ.get("SUBJECT_KEYWORD", "Support")
    reply_body = os.environ.get("REPLY_BODY", "Thanks — we've received your message and will respond shortly.")
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    q = f"https://graph.microsoft.com/v1.0/me/messages?$filter=isRead eq false and contains(subject,'{keyword}')&$top=10"
    resp = requests.get(q, headers=headers)
    if not resp.ok:
        print("Query failed", resp.status_code, resp.text); return

    for m in resp.json().get("value", []):
        mid = m["id"]
        to = [{"emailAddress": {"address": a.get("emailAddress", {}).get("address")}} for a in m.get("from", {}) and [m["from"]] or m.get("toRecipients", [])]
        # Create reply message and send
        mail = {
            "message": {
                "subject": f"Re: {m.get('subject')}",
                "body": {"contentType": "Text", "content": reply_body},
                "toRecipients": to
            },
            "saveToSentItems": "true"
        }
        send = requests.post(f"https://graph.microsoft.com/v1.0/me/messages/{mid}/reply", headers=headers, json={"message": mail["message"], "comment": reply_body})
        # mark as read
        requests.patch(f"https://graph.microsoft.com/v1.0/me/messages/{mid}", headers=headers, json={"isRead": True})
        print("Replied to:", m.get("subject"), "status:", send.status_code)

if __name__ == "__main__":
    run()
