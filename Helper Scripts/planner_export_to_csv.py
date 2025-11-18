# planner_export_to_csv.py
import os, requests, csv, io
from helper_auth import get_token

def run():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # list user's plans
    plans = requests.get("https://graph.microsoft.com/v1.0/me/planner/plans", headers=headers).json().get("value", [])
    if not plans:
        print("No plans found"); return
    plan_id = plans[0]["id"]

    tasks = requests.get(f"https://graph.microsoft.com/v1.0/planner/plans/{plan_id}/tasks", headers=headers).json().get("value", [])
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["id","title","assignedTo","dueDateTime","percentComplete"])
    for t in tasks:
        assignments = ",".join(t.get("assignments",{}).keys())
        writer.writerow([t.get("id"), t.get("title"), assignments, t.get("dueDateTime"), t.get("percentComplete")])

    csv_bytes = buf.getvalue().encode("utf-8")
    put = requests.put("https://graph.microsoft.com/v1.0/me/drive/root:/planner_export.csv:/content", headers={**headers, "Content-Type":"text/csv"}, data=csv_bytes)
    print("Saved planner_export.csv:", put.status_code)

if __name__ == "__main__":
    run()
