# delta_users.py
import requests
from helper_auth import get_token

token = get_token()
headers = {"Authorization": f"Bearer {token}"}

# initial call: https://graph.microsoft.com/v1.0/users/delta
url = "https://graph.microsoft.com/v1.0/users/delta?$select=id,displayName,mail,userPrincipalName"
resp = requests.get(url, headers=headers)
if resp.ok:
    data = resp.json()
    for u in data.get("value", []):
        print("User:", u.get("displayName"), u.get("userPrincipalName"))
    # Save @odata.nextLink or @odata.deltaLink for subsequent incremental calls
    print("Next/Delta link:", data.get("@odata.nextLink") or data.get("@odata.deltaLink"))
else:
    print(resp.status_code, resp.text)
