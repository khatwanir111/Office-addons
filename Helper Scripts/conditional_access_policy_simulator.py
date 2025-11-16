import requests
from helper_auth import get_token

def create_policy():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    payload = {
        "displayName": "AutoDevPolicy",
        "state": "disabled",
        "conditions": {"users": {"includeUsers": ["All"]}},
        "grantControls": {"operator": "OR", "builtInControls": ["mfa"]},
    }

    resp = requests.post(
        "https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies",
        headers=headers, json=payload
    )
    print(resp.status_code, resp.text)


if __name__ == "__main__":
    create_policy()
