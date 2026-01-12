import os,csv,requests,msal

TENANT_ID=os.getenv("M365_TENANT_ID")
CLIENT_ID=os.getenv("M365_CLIENT_ID")
CLIENT_SECRET=os.getenv("M365_CLIENT_SECRET")
OUTPUT="group_mail_settings.csv"
SCOPES=["https://graph.microsoft.com/.default"]

def token():
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    ).acquire_token_for_client(SCOPES)["access_token"]

def main():
    headers={"Authorization":f"Bearer {token()}"}
    r=requests.get("https://graph.microsoft.com/v1.0/groups?$select=displayName,mail,mailEnabled,securityEnabled",headers=headers)
    r.raise_for_status()
    rows=[]
    for g in r.json().get("value",[]):
        rows.append({
            "group":g.get("displayName"),
            "mail":g.get("mail"),
            "mailEnabled":g.get("mailEnabled"),
            "securityEnabled":g.get("securityEnabled")
        })
    with open(OUTPUT,"w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print("Exported",len(rows),"groups")

if __name__=="__main__":
    main()
