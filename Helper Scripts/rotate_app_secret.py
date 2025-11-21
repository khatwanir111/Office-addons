# rotate_app_secret.py
# ENV: TARGET_APP_ID (the appId of the application to rotate), KEEP_DAYS (optional, default 30)
import os, requests, json
from datetime import datetime, timedelta
from helper_auth import get_token

def run():
    app_id = os.environ.get("TARGET_APP_ID")
    keep_days = int(os.environ.get("KEEP_DAYS", "30"))
    if not app_id:
        print("Set TARGET_APP_ID in env"); return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    # 1) find application object by appId
    r = requests.get(f"https://graph.microsoft.com/v1.0/applications?$filter=appId eq '{app_id}'", headers=headers)
    if not r.ok or not r.json().get("value"):
        print("App not found or permission missing:", r.status_code, r.text); return
    app_obj = r.json()["value"][0]
    app_object_id = app_obj["id"]

    # 2) create new client secret (password)
    end = (datetime.utcnow() + timedelta(days=90)).isoformat() + "Z"
    payload = {"passwordCredential": {"displayName":"rotated-secret", "endDateTime": end, "startDateTime": datetime.utcnow().isoformat() + "Z"}}
    secret_resp = requests.post(f"https://graph.microsoft.com/v1.0/applications/{app_object_id}/addPassword", headers=headers, json=payload)
    if not secret_resp.ok:
        print("Failed to add secret:", secret_resp.status_code, secret_resp.text); return
    secret_text = secret_resp.json().get("secretText")
    print("New secret (copy now):", secret_text)

    # 3) remove old secrets older than keep_days
    keep_cutoff = datetime.utcnow() - timedelta(days=keep_days)
    # fetch app to inspect passwordCredentials
    app_full = requests.get(f"https://graph.microsoft.com/v1.0/applications/{app_object_id}", headers=headers).json()
    pw_creds = app_full.get("passwordCredentials", [])
    for cred in pw_creds:
        start = cred.get("startDateTime")
        try:
            sd = datetime.fromisoformat(start.replace("Z", "+00:00"))
        except Exception:
            continue
        if sd < keep_cutoff:
            # remove by keyId via removePassword
            rem_payload = {"keyId": cred.get("keyId")}
            rem = requests.post(f"https://graph.microsoft.com/v1.0/applications/{app_object_id}/removePassword", headers=headers, json=rem_payload)
            print("Removed old credential:", cred.get("displayName"), rem.status_code)
    print("Rotation complete.")

if __name__ == "__main__":
    run()
