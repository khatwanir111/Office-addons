# helper_auth.py
from msal import PublicClientApplication
import os

def get_token():
    app = PublicClientApplication(
        os.environ["CLIENT_ID"],
        authority=f"https://login.microsoftonline.com/{os.environ['TENANT_ID']}"
    )
    result = app.acquire_token_by_username_password(
        os.environ["USERNAME"],
        os.environ["PASSWORD"],
        scopes=["https://graph.microsoft.com/.default"]
    )
    if "access_token" not in result:
        raise Exception(result.get("error_description"))
    return result["access_token"]
