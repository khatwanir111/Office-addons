# apply_sensitivity_label.py
import os, requests
from helper_auth import get_token

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# File item id in OneDrive or SharePoint
ITEM_ID = os.environ.get("ITEM_ID")
LABEL_ID = os.environ.get("SENSITIVITY_LABEL_ID")  # an existing label ID in tenant

if not ITEM_ID or not LABEL_ID:
    print("Set ITEM_ID and SENSITIVITY_LABEL_ID env vars.")
    exit(0)

payload = {"application": {"id": LABEL_ID}}
# Graph endpoint to apply sensitivity label varies; using the driveItem endpoint for demonstration:
resp = requests.post(f"https://graph.microsoft.com/v1.0/me/drive/items/{ITEM_ID}/applySensitivityLabel", headers=headers, json=payload)
print(resp.status_code, resp.text)
