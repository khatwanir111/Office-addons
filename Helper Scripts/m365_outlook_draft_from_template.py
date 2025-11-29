import os
import json
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")

SCOPES = ["https://graph.microsoft.com/.default"]
TEMPLATE_FILE = "email_template.json"

DEFAULT_TEMPLATE = {
    "subject": "M365 Dev Update",
    "body": "Hi,\n\nHere is the latest update on our Microsoft 365 development work.\n\nThanks.",
    "to": ["someone@example.com"],
}

def get_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET,
    )
    result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" not in result:
        raise RuntimeError(f"Token error: {result.get('error_description')}")
    return result["access_token"]

def load_template():
    if not os.path.exists(TEMPLATE_FILE):
        with open(TEMPLATE_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_TEMPLATE, f, indent=2)
        print(f"Template created: {TEMPLATE_FILE}")
        return DEFAULT_TEMPLATE

    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def create_draft():
    tpl = load_template()
    token = get_token()

    url = "https://graph.microsoft.com/v1.0/me/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload = {
        "subject": tpl["subject"],
        "body": {"contentType": "Text", "content": tpl["body"]},
        "toRecipients": [{"emailAddress": {"address": addr}} for addr in tpl["to"]],
    }

    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    print("Draft created:", resp.json().get("id"))

if __name__ == "__main__":
    create_draft()
