import os, requests, msal

TENANT_ID = os.getenv("M365_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET")
ROLE_TEMPLATE_ID = "ROLE_TEMPLATE_ID"
USER_OBJECT_ID = "USER_OBJECT_ID"
SCOPES = ["https://graph.microsoft.com/.default"]

def token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET,
    )
    return app.acquire_token_for_client(SCOPES)["access_token"]

def main():
    headers = {"Authorization": f"Bearer {token()}", "Content-Type": "application/json"}
    activate = requests.post(
        "https://graph.microsoft.com/v1.0/directoryRoles",
        headers=headers,
        json={"roleTemplateId": ROLE_TEMPLATE_ID},
    )
    if activate.status_code not in (201, 409):
        activate.raise_for_status()

    roles = requests.get(
        "https://graph.microsoft.com/v1.0/directoryRoles",
        headers=headers,
    ).json()["value"]

    role_id = next(r["id"] for r in roles if r["roleTemplateId"] == ROLE_TEMPLATE_ID)

    assign = requests.post(
        f"https://graph.microsoft.com/v1.0/directoryRoles/{role_id}/members/$ref",
        headers=headers,
        json={"@odata.id": f"https://graph.microsoft.com/v1.0/users/{USER_OBJECT_ID}"},
    )
    assign.raise_for_status()
    print("Role assigned")

if __name__ == "__main__":
    main()
