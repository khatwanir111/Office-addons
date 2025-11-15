# planner_move_task_between_buckets.py
import os, requests
from helper_auth import get_token

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# pick a plan
plans = requests.get("https://graph.microsoft.com/v1.0/me/planner/plans", headers=headers).json().get("value", [])
if not plans:
    print("No planner plans found.")
    exit(0)
plan_id = plans[0]["id"]

# get buckets
buckets = requests.get(f"https://graph.microsoft.com/v1.0/planner/plans/{plan_id}/buckets", headers=headers).json().get("value", [])
if len(buckets) < 2:
    print("Need at least two buckets; found:", len(buckets))
    exit(0)

source_bucket = buckets[0]["id"]
dest_bucket = buckets[1]["id"]

# find a task in source bucket
tasks = requests.get(f"https://graph.microsoft.com/v1.0/planner/buckets/{source_bucket}/tasks", headers=headers).json().get("value", [])
if not tasks:
    print("No tasks in source bucket.")
    exit(0)
task = tasks[0]

# move task: update bucketId using the ETag for concurrency
task_id = task["id"]
etag = task["@odata.etag"]
update = {"bucketId": dest_bucket}
resp = requests.patch(f"https://graph.microsoft.com/v1.0/planner/tasks/{task_id}", headers={**headers, "If-Match": etag}, json=update)
print("Move response:", resp.status_code)
