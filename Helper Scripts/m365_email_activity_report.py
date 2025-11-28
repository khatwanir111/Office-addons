# m365_email_activity_report.py
# ENV: PERIOD (e.g. "D7","D30","D90")
import os, requests
from helper_auth import get_token

def run():
    period = os.environ.get("PERIOD", "D7")
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    url = f"https://graph.microsoft.com/v1.0/reports/getEmailActivityUserDetail(period='{period}')"
    resp = requests.get(url, headers=headers)
    if not resp.ok:
        print("Report fetch failed:", resp.status_code, resp.text)
        return

    filename = f"email_activity_{period}.csv"
    put = requests.put(
        f"https://graph.microsoft.com/v1.0/me/drive/root:/{filename}:/content",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "text/csv"},
        data=resp.content
    )
    print("Saved", filename, "status:", put.status_code)

if __name__ == "__main__":
    run()
