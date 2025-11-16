import os, requests
from helper_auth import get_token

def assign_role(user_id, role_name="User Account Administrator"):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    roles = requests.get("https://graph.microsoft.com/v1.0/directoryRoles", headers=headers).json().get("value", [])
    role = next((r for r in roles if r["displayName"] == role_name), None)

    if not role:
        print("Role not active.")
        return

    role_id = role["id"]
    payload = {"@odata.id": f"https://graph.microsoft.com/v1.0/directoryObjects/{user_id}"}
    resp = requests.post(
        f"https://graph.microsoft.com/v1.0/directoryRoles/{role_id}/members/$ref",
        headers=headers, json=payload
    )
    print(resp.status_code, resp.text)


if __name__ == "__main__":
    assign_role(os.environ.get("TARGET_USER_ID"))
