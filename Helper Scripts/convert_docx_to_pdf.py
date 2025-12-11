import os
import requests
import msal
from pathlib import Path

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")
USER_ID = "user@domain.com"
ITEM_ID = "DRIVE_ITEM_ID"  # OneDrive item id for the docx
OUTPUT_FILE = "output.pdf"

SCOPES = ["https://graph.microsoft.com/.default"]

def get_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(SCOPES)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))
    return result["access_token"]

def convert_to_pdf():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    # Graph supports format conversion with ?format=pdf on the /content endpoint
    url = f"https://graph.microsoft.com/v1.0/users/{USER_ID}/drive/items/{ITEM_ID}/content?format=pdf"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    Path(OUTPUT_FILE).write_bytes(resp.content)
    print("Saved converted PDF to", OUTPUT_FILE)

if __name__ == "__main__":
    convert_to_pdf()
