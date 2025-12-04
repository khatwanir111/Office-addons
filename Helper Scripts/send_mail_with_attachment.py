import os
import base64
import requests
import msal
from pathlib import Path

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")

USER_ID = "user@domain.com"
SCOPES = ["https://graph.microsoft.com/.default"]

ATTACH_FILE = "example.txt"
TO_ADDRESS = "someone@example.com"

def get_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET,
    )
    result = app.acquire_token_for_client(SCOPES)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))
    return result["access_token"]

def send_mail():
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    content_bytes = Path(ATTACH_FILE).read_bytes()
    content_b64 = base64.b64encode(content_bytes).decode("utf-8")

    message = {
        "message": {
            "subject": "Mail from Graph with attachment",
            "body": {
                "contentType": "Text",
                "content": "Please find the attachment.",
            },
            "toRecipients": [
                {"emailAddress": {"address": TO_ADDRESS}}
            ],
            "attachments": [
                {
                    "@odata.type": "#microsoft.graph.fileAttachment",
                    "name": ATTACH_FILE,
                    "contentBytes": content_b64,
                }
            ],
        },
        "saveToSentItems": True,
    }

    url = f"https://graph.microsoft.com/v1.0/users/{USER_ID}/sendMail"
    resp = requests.post(url, headers=headers, json=message)
    resp.raise_for_status()
    print("Mail sent.")

if __name__ == "__main__":
    send_mail()
