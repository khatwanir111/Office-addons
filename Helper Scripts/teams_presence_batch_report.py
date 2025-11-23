# teams_presence_batch_report.py
# ENV: USER_UPNS (comma-separated list)
import os, requests, json
from helper_auth import get_token

def run():
    upns = [u.strip() for u in os.environ.get("USER_UPNS", "").split(",") if u.strip()]
    if not upns:
        print("Set USER_UPNS"); return
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    # build batch requests to /users/{id or upn}/presence
    requests_payload = []
    for i, upn in enumerate(upns, start=1):
        requests_payload.append({"id": str(i), "method":"GET", "url": f"/users/{upn}/presence"})

    batch = {"requests": requests_payload}
    resp = requests.post("https://graph.microsoft.com/v1.0/$batch", headers=headers, json=batch)
    if not resp.ok:
        print("Batch failed", resp.status_code, resp.text); return

    out = resp.json()
    # save to OneDrive
    requests.put("https://graph.microsoft.com/v1.0/me/drive/root:/presence_report.json:/content", headers={**headers, "Content-Type":"application/json"}, data=json.dumps(out).encode("utf-8"))
    print("Saved presence_report.json")

if __name__ == "__main__":
    run()
