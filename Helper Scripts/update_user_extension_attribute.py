# update_user_extension_attribute.py
# ENV: TARGET_UPN, ATTRIBUTE_NAME (e.g. "extensionAttribute1"), ATTRIBUTE_VALUE
import os, requests
from helper_auth import get_token

def run():
    upn = os.environ.get("TARGET_UPN")
    attr = os.environ.get("ATTRIBUTE_NAME", "extensionAttribute1")
    value = os.environ.get("ATTRIBUTE_VALUE", "AutoFlag")
    if not upn:
        print("Set TARGET_UPN")
        return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    payload = {"onPremisesExtensionAttributes": {attr: value}}
    resp = requests.patch(f"https://graph.microsoft.com/v1.0/users/{upn}", headers=headers, json=payload)
    print("Update extension attr status:", resp.status_code, resp.text)

if __name__ == "__main__":
    run()
