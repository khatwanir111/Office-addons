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
    headers={"Authorization":f"Bearer {token()}","ConsistencyLevel":"eventual"}
    risky=len(requests.get("https://graph.microsoft.com/v1.0/identityProtection/riskyUsers",headers=headers).json().get("value",[]))
    failures=len(requests.get("https://graph.microsoft.com/v1.0/auditLogs/signIns?$filter=status/errorCode ne 0",headers=headers).json().get("value",[]))
    policies=len(requests.get("https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies",headers=headers).json().get("value",[]))
    print("Risky users:",risky)
    print("Failed sign-ins:",failures)
    print("Conditional access policies:",policies)

if __name__=="__main__":
    main()
