# create_planner_task.py
import requests, json
from helper_auth import get_token

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# You need a planId and bucketId — this example lists plans for the user and picks the first
plans = requests.get("https://graph.microsoft.com/v1.0/me/planner/plans", headers=headers).json()
plan_items = plans.get("value", [])
if not plan_items:
    print("No plans found for user.")
else:
    plan_id = plan_items[0]["id"]
    # get buckets for plan
    buckets = requests.get(f"https://graph.microsoft.com/v1.0/planner/plans/{plan_id}/buckets", headers=headers).json()
    bucket_id = buckets.get("value", [{}])[0].get("id")
    task_payload = {"planId": plan_id, "bucketId": bucket_id, "title": "Automated Task - Dev Script"}
    task_resp = requests.post("https://graph.microsoft.com/v1.0/planner/tasks", headers=headers, json=task_payload)
    print(task_resp.status_code, task_resp.text)
