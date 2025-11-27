# todo_create_tasks_from_csv.py
# ENV: CSV_ONEDRIVE_PATH (optional, e.g. "/tasks.csv"), LOCAL_CSV (fallback)
import os, requests, io, csv
from helper_auth import get_token

def fetch_csv_from_onedrive(path, token):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"https://graph.microsoft.com/v1.0/me/drive/root:{path}:/content", headers=headers)
    return r.content.decode() if r.ok else None

def run():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    csv_path = os.environ.get("CSV_ONEDRIVE_PATH")
    local_csv = os.environ.get("LOCAL_CSV", "tasks.csv")

    data = None
    if csv_path:
        data = fetch_csv_from_onedrive(csv_path, token)
    if not data and os.path.exists(local_csv):
        data = open(local_csv, "r", encoding="utf-8").read()
    if not data:
        print("No CSV found")
        return

    # Ensure default task list
    lists = requests.get("https://graph.microsoft.com/v1.0/me/todo/lists", headers=headers).json().get("value", [])
    if lists:
        list_id = lists[0]["id"]
    else:
        create_list = requests.post("https://graph.microsoft.com/v1.0/me/todo/lists", headers=headers, json={"displayName":"Auto Tasks"})
        list_id = create_list.json()["id"]

    reader = csv.DictReader(io.StringIO(data))
    for row in reader:
        title = row.get("title") or row.get("subject") or "Untitled"
        body = row.get("body") or ""
        payload = {"title": title, "body": {"content": body, "contentType":"text"}}
        r = requests.post(f"https://graph.microsoft.com/v1.0/me/todo/lists/{list_id}/tasks", headers=headers, json=payload)
        print("Create task:", title, r.status_code)

if __name__ == "__main__":
    run()
