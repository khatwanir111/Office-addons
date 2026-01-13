import os,requests,msal
from datetime import datetime,timezone

TENANT_ID=os.getenv("M365_TENANT_ID")
CLIENT_ID=os.getenv("M365_CLIENT_ID")
CLIENT_SECRET=os.getenv("M365_CLIENT_SECRET")
SCOPES=["https://graph.microsoft.com/.default"]

def token():
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    ).acquire_token_for_client(SCOPES)["access_token"]

def main():
    headers={"Authorization":f"Bearer {token()}"}
    apps=requests.get("https://graph.microsoft.com/v1.0/applications?$select=displayName,passwordCredentials",headers=headers).json()["value"]
    now=datetime.now(timezone.utc)
    for a in apps:
        for c in a.get("passwordCredentials",[]):
            if c.get("endDateTime"):
                dt=datetime.fromisoformat(c["endDateTime"].replace("Z","+00:00"))
                if dt<now:
                    print(a.get("displayName"),"| expired")

if __name__=="__main__":
    main()
