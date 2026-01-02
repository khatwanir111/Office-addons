import os, csv, requests, msal

TENANT_ID=os.getenv("M365_TENANT_ID")
CLIENT_ID=os.getenv("M365_CLIENT_ID")
CLIENT_SECRET=os.getenv("M365_CLIENT_SECRET")
OUTPUT="group_member_counts.csv"
SCOPES=["https://graph.microsoft.com/.default"]

def token():
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    ).acquire_token_for_client(SCOPES)["access_token"]

def main():
    headers={"Authorization":f"Bearer {token()}"}
    groups=requests.get("https://graph.microsoft.com/v1.0/groups",headers=headers).json()["value"]
    rows=[]
    for g in groups:
        count=requests.get(
            f"https://graph.microsoft.com/v1.0/groups/{g['id']}/members/$count",
            headers={**headers,"ConsistencyLevel":"eventual"}
        ).text
        rows.append({"group":g.get("displayName"),"memberCount":count})

    with open(OUTPUT,"w",newline="",encoding="utf-8") as f:
        csv.DictWriter(f,rows[0].keys()).writeheader() or csv.DictWriter(f,rows[0].keys()).writerows(rows)

    print("Exported",len(rows),"groups")

if __name__=="__main__":
    main()
