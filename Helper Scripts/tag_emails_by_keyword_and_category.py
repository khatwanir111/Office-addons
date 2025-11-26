# tag_emails_by_keyword_and_category.py
# ENV: KEYWORD (e.g. "urgent"), CATEGORY (e.g. "Urgent")
import os, requests
from datetime import datetime, timedelta
from helper_auth import get_token

def run():
    keyword = os.environ.get("KEYWORD", "urgent")
    category = os.environ.get("CATEGORY", "Auto-Urgent")

    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    since = (datetime.utcnow() - timedelta(days=3)).isoformat() + "Z"
    url = f"https://graph.microsoft.com/v1.0/me/messages?$filter=receivedDateTime ge {since}&$top=50"
    resp = requests.get(url, headers=headers)
    if not resp.ok:
        print("Message fetch failed:", resp.status_code, resp.text)
        return

    for msg in resp.json().get("value", []):
        subject = msg.get("subject", "") or ""
        body_preview = msg.get("bodyPreview", "") or ""
        if keyword.lower() in subject.lower() or keyword.lower() in body_preview.lower():
            mid = msg["id"]
            cats = msg.get("categories", [])
            if category not in cats:
                cats.append(category)
                upd = requests.patch(
                    f"https://graph.microsoft.com/v1.0/me/messages/{mid}",
                    headers=headers,
                    json={"categories": cats}
                )
                print("Tagged:", subject[:40], upd.status_code)

if __name__ == "__main__":
    run()
