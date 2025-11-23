# sharepoint_add_column_with_validation.py
# ENV: SITE_ID (optional), LIST_NAME (e.g., ProjectTasks), COLUMN_NAME, CHOICES (comma-separated)
import os, requests
from helper_auth import get_token

def run():
    site_id = os.environ.get("SITE_ID")  # optional; if missing uses root site
    list_name = os.environ.get("LIST_NAME", "ProjectTasks")
    col_name = os.environ.get("COLUMN_NAME", "Severity")
    choices = [c.strip() for c in os.environ.get("CHOICES", "Low,Medium,High").split(",")]

    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    base = f"https://graph.microsoft.com/v1.0/sites/{site_id}" if site_id else "https://graph.microsoft.com/v1.0/sites/root"
    # find list
    lists = requests.get(f"{base}/lists", headers=headers).json().get("value", [])
    target = next((l for l in lists if l.get("displayName")==list_name), None)
    if not target:
        print("List not found:", list_name); return
    list_id = target["id"]

    payload = {
        "name": col_name,
        "choice": {"choices": choices}
    }
    resp = requests.post(f"{base}/lists/{list_id}/columns", headers=headers, json=payload)
    print("Add column status:", resp.status_code, resp.text)

if __name__ == "__main__":
    run()
