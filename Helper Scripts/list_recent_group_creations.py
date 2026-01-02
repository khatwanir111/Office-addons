import os,requests,msal
from datetime import datetime,timedelta,timezone

TENANT_ID=os.getenv("M365_TENANT_ID")
CLIENT_ID=os.getenv("M365_CLIENT_ID")
CLIENT_SECRET=os.getenv("M365_CLIENT_SECRET")
DAYS=7
SCOPES=["https://graph.microsoft.com/.default"]

def token():
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    ).acquire_token_for_client(SCOPES)["access_token"]

def main():
    headers={"Authorization":f"Bearer {token()}"}
    cutoff=datetime.now(timezone.utc)-timedelta(days=DAYS)
    groups=requests.get("https://graph.microsoft.com/v1.0/groups?$select=displayName,createdDateTime",headers=headers).json()["value"]
    for g in groups:
        if g.get("createdDateTime"):
            dt=datetime.fromisoformat(g["createdDateTime"].replace("Z","+00:00"))
            if dt>cutoff:
                print(g.get("displayName"),"|",g.get("createdDateTime"))

if __name__=="__main__":
    main()
