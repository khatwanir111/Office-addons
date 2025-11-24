# find_unused_service_principals.py
import requests, json
from helper_auth import get_token

def run():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    sps = []
    url = "https://graph.microsoft.com/v1.0/servicePrincipals?$top=50"
    while url:
        r = requests.get(url, headers=headers)
        if not r.ok:
            print("Failed listing SPs"); return
        data = r.json()
        for sp in data.get("value", []):
            owners = requests.get(f"https://graph.microsoft.com/v1.0/servicePrincipals/{sp['id']}/owners", headers=headers)
            owner_count = len(owners.json().get("value", [])) if owners.ok else "?"
            if owner_count == 0:
                sps.append({"id": sp["id"], "displayName": sp.get("displayName"), "appId": sp.get("appId")})
        url = data.get("@odata.nextLink")
    # save
    put = requests.put("https://graph.microsoft.com/v1.0/me/drive/root:/unused_service_principals.json:/content",
                       headers={**headers, "Content-Type":"application/json"}, data=json.dumps(sps).encode("utf-8"))
    print("Saved report:", put.status_code)

if __name__ == "__main__":
    run()
