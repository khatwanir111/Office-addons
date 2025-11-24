# send_mail_with_attachments_from_onedrive.py
# ENV: FILE_PATH (OneDrive path, e.g. /Reports/report.pdf), TO (comma-separated)
import os, base64, requests
from helper_auth import get_token

def run():
    file_path = os.environ.get("FILE_PATH")
    to_list = [t.strip() for t in os.environ.get("TO", "").split(",") if t.strip()]
    if not (file_path and to_list):
        print("Set FILE_PATH and TO"); return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # download file content
    r = requests.get(f"https://graph.microsoft.com/v1.0/me/drive/root:{file_path}:/content", headers=headers)
    if not r.ok:
        print("Failed to download file", r.status_code, r.text); return
    content_bytes = base64.b64encode(r.content).decode()

    attachment = {
        "@odata.type": "#microsoft.graph.fileAttachment",
        "name": os.path.basename(file_path),
        "contentBytes": content_bytes
    }

    message = {
        "message": {
            "subject": "Automated mail with attachment",
            "body": {"contentType": "Text", "content": "See attached file."},
            "toRecipients": [{"emailAddress": {"address": a}} for a in to_list],
            "attachments": [attachment]
        },
        "saveToSentItems": "true"
    }

    resp = requests.post("https://graph.microsoft.com/v1.0/me/sendMail", headers={**headers, "Content-Type":"application/json"}, json=message)
    print("Send mail status:", resp.status_code, resp.text)

if __name__ == "__main__":
    run()
