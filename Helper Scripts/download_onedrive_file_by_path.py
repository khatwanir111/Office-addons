import os
import requests
import msal
from pathlib import Path

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")

USER_ID = "user@domain.com"
SCOPES = ["https://graph.microsoft.com/.default"]

FILE_PATH = "/Documents/Report.xlsx"  # OneDrive path
LOCAL_NAME = "Report_downloaded.xlsx"

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

def download_file():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = (
        f"https://graph.microsoft.com/v1.0/users/{USER_ID}"
        f"/drive/root:{FILE_PATH}:/content"
    )

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    Path(LOCAL_NAME).write_bytes(resp.content)
    print("Downloaded to:", LOCAL_NAME)

if __name__ == "__main__":
    download_file()
