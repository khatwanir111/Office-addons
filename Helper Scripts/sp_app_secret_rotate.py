# sp_app_secret_rotate.py
import requests
from helper_auth import get_token
from datetime import datetime, timedelta
import os

def rotate_secret(app_object_id):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    payload = {
        "passwordCredential": {
            "displayName": "rotated-by-script",
            "startDateTime": datetime.utcnow().isoformat() + "Z",
            "endDateTime": (datetime.utcnow() + timedelta(days=90)).isoformat() + "Z"
        }
    }

    r = requests.post(f"https://graph.microsoft.com/v1.0/applications/{app_object_id}/addPassword", headers=headers, json=payload)
    if not r.ok:
        print("Failed to add secret:", r.status_code, r.text); return
    secret = r.json()
    print("New secret value (copy now):", secret.get("secretText"))

    # Optionally remove old credentials by listing and removing by id (skipped here—requires careful selection)
    print("Rotation complete. Remember to store the value securely.")


if __name__ == "__main__":
    # Provide APP_OBJECT_ID via env var or edit here
    app_obj = os.environ.get("APP_OBJECT_ID")
    if not app_obj:
        print("Set APP_OBJECT_ID environment variable to the application's object id.")
    else:
        rotate_secret(app_obj)
