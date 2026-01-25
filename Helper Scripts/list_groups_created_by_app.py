import os,requests,msal

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
    r=requests.get(
        "https://graph.microsoft.com/v1.0/groups?$select=displayName,createdByAppId",
        headers=headers
    )
    r.raise_for_status()
    for g in r.json().get("value",[]):
        if g.get("createdByAppId"):
            print(g.get("displayName"),"|",g.get("createdByAppId"))

if __name__=="__main__":
    main()
