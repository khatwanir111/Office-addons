import os
import csv
import requests
import msal

TENANT_ID = os.getenv("M365_TENANT_ID", "YOUR_TENANT_ID")
CLIENT_ID = os.getenv("M365_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET", "YOUR_CLIENT_SECRET")
PLAN_ID = "YOUR_PLANNER_PLAN_ID"

SCOPES = ["https://graph.microsoft.com/.default"]
OUTPUT_CSV = "planner_tasks.csv"

def get_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET,
    )
    result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" not in result:
        raise RuntimeError(f"Token error: {result.get('error_description')}")
    return result["access_token"]

def export_tasks():
    token = get_token()
    url = f"https://graph.microsoft.com/v1.0/planner/plans/{PLAN_ID}/tasks"
    headers = {"Authorization": f"Bearer {token}"}

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    tasks = resp.json().get("value", [])

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "title", "percentComplete"])
        for t in tasks:
            writer.writerow([
                t.get("id"),
                t.get("title"),
                t.get("percentComplete"),
            ])

    print(f"Exported {len(tasks)} tasks to {OUTPUT_CSV}")

if __name__ == "__main__":
    export_tasks()
