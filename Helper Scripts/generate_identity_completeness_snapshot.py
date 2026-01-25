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
    users=requests.get(
        "https://graph.microsoft.com/v1.0/users?$select=jobTitle,department,usageLocation,officeLocation",
        headers=headers
    ).json()["value"]

    total=len(users)
    job=sum(1 for u in users if u.get("jobTitle"))
    dept=sum(1 for u in users if u.get("department"))
    usage=sum(1 for u in users if u.get("usageLocation"))

    print("Total users:",total)
    print("With job title:",job)
    print("With department:",dept)
    print("With usage location:",usage)

if __name__=="__main__":
    main()
