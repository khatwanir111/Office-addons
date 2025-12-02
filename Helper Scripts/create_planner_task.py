import os
import requests
import msal
from datetime import datetime, timedelta

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")

SCOPES = ["https://graph.microsoft.com/.default"]
PLAN_ID = "YOUR_PLAN_ID"
BUCKET_ID = "YOUR_BUCKET_ID"

def get_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET,
    )
    result = app.acquire_token_for_client(SCOPES)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description"))
    return result["access_token"]

def create_task(title="Dev Task from Script"):
    token = get_token()
    url = "https://graph.microsoft.com/v1.0/planner/tasks"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    due = (datetime.utcnow() + timedelta(days=2)).isoformat() + "Z"
    payload = {
        "planId": PLAN_ID,
        "bucketId": BUCKET_ID,
        "title": title,
        "dueDateTime": due,
    }
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    print("Task created:", resp.json().get("id"))

if __name__ == "__main__":
    create_task()
