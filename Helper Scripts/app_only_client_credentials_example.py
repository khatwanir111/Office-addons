# app_only_client_credentials_example.py
import os, requests

def run():
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    tenant = os.environ.get("TENANT_ID")
    if not (client_id and client_secret and tenant):
        print("Set CLIENT_ID, CLIENT_SECRET, TENANT_ID for app-only auth"); return

    token_url = f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
    data = {"grant_type":"client_credentials","client_id":client_id,"client_secret":client_secret,"scope":"https://graph.microsoft.com/.default"}
    r = requests.post(token_url, data=data)
    if not r.ok:
        print("Token fetch failed:", r.status_code, r.text); return
    token = r.json().get("access_token")
    print("Got app-only token (len):", len(token or ""))

    # Example call: list service principals
    headers = {"Authorization": f"Bearer {token}"}
    sp = requests.get("https://graph.microsoft.com/v1.0/servicePrincipals?$top=5", headers=headers)
    print("Service principals status:", sp.status_code, sp.text[:400])

if __name__ == "__main__":
    run()
