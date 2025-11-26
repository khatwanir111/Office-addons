# notify_if_mailbox_over_threshold.py
# ENV: MESSAGE_COUNT_THRESHOLD (default 10000)
import os, requests
from helper_auth import get_token

def run():
    threshold = int(os.environ.get("MESSAGE_COUNT_THRESHOLD", "10000"))
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Very rough proxy: sum of item counts in top-level folders
    r = requests.get("https://graph.microsoft.com/v1.0/me/mailFolders?$top=50", headers=headers)
    if not r.ok:
        print("Folder list failed:", r.status_code, r.text)
        return
    total = 0
    for f in r.json().get("value", []):
        fid = f["id"]
        fr = requests.get(f"https://graph.microsoft.com/v1.0/me/mailFolders/{fid}?$select=totalItemCount", headers=headers)
        if fr.ok:
            total += fr.json().get("totalItemCount", 0)

    print("Estimated total messages:", total)

    if total > threshold:
        # send warning mail to self
        me = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers).json()
        my_mail = me.get("mail") or me.get("userPrincipalName")
        message = {
            "message": {
                "subject": "Mailbox threshold exceeded",
                "body": {"contentType": "Text", "content": f"Estimated total messages: {total} (threshold {threshold})."},
                "toRecipients": [{"emailAddress": {"address": my_mail}}],
            },
            "saveToSentItems": "true"
        }
        send = requests.post("https://graph.microsoft.com/v1.0/me/sendMail",
                             headers={**headers, "Content-Type": "application/json"},
                             json=message)
        print("Sent warning:", send.status_code)
    else:
        print("Mailbox under threshold.")

if __name__ == "__main__":
    run()
