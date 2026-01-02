import os,csv,requests,msal

TENANT_ID=os.getenv("M365_TENANT_ID")
CLIENT_ID=os.getenv("M365_CLIENT_ID")
CLIENT_SECRET=os.getenv("M365_CLIENT_SECRET")
OUTPUT="drive_usage.csv"
SCOPES=["https://graph.microsoft.com/.default"]

def token():
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    ).acquire_token_for_client(SCOPES)["access_token"]

def main():
    headers={"Authorization":f"Bearer {token()}"}
    users=requests.get("https://graph.microsoft.com/v1.0/users?$select=id,displayName",headers=headers).json()["value"]
    rows=[]
    for u in users:
        r=requests.get(f"https://graph.microsoft.com/v1.0/users/{u['id']}/drive",headers=headers)
        if r.status_code==200:
            q=r.json().get("quota",{})
            rows.append({
                "user":u.get("displayName"),
                "used":q.get("used"),
                "total":q.get("total")
            })

    with open(OUTPUT,"w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("Exported drive usage for",len(rows),"users")

if __name__=="__main__":
    main()
