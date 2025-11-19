# export_planner_chart_png.py
import os, requests, io
from helper_auth import get_token
import json

def run():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    plans_resp = requests.get("https://graph.microsoft.com/v1.0/me/planner/plans", headers=headers)
    plans = plans_resp.json().get("value", [])
    if not plans:
        print("No planner plans found"); return
    plan_id = plans[0]["id"]

    tasks = requests.get(f"https://graph.microsoft.com/v1.0/planner/plans/{plan_id}/tasks", headers=headers).json().get("value", [])
    counts = {"total": len(tasks), "completed": sum(1 for t in tasks if t.get("percentComplete",0)==100)}

    # Create a tiny placeholder PNG bytes (real charting would use matplotlib locally)
    png_bytes = b"\x89PNG\r\n\x1a\n" + json.dumps(counts).encode()  # placeholder, not a real PNG file
    filename = "planner_chart_placeholder.png"
    put = requests.put(f"https://graph.microsoft.com/v1.0/me/drive/root:/{filename}:/content", headers={**headers, "Content-Type":"image/png"}, data=png_bytes)
    print("Saved chart placeholder:", put.status_code)

if __name__ == "__main__":
    run()
