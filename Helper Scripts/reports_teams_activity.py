# reports_teams_activity.py
import requests
from helper_auth import get_token

def fetch_teams_report():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://graph.microsoft.com/v1.0/reports/getTeamsUserActivityUserDetail(period='D7')"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        requests.put("https://graph.microsoft.com/v1.0/me/drive/root:/teams_activity.csv:/content",
                     headers={"Authorization": f"Bearer {token}"}, data=r.content)
        print("Saved Teams activity report to OneDrive.")
    else:
        print("Failed to fetch report:", r.status_code, r.text)

if __name__ == "__main__":
    fetch_teams_report()
