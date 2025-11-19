# install_teams_app_to_team.py
import os, requests
from helper_auth import get_token

def run():
    app_id = os.environ.get("TEAMS_APP_ID")
    team_id = os.environ.get("TEAM_ID")
    if not app_id or not team_id:
        print("Set TEAMS_APP_ID and TEAM_ID in env"); return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    payload = {"teamsApp@odata.bind": f"https://graph.microsoft.com/v1.0/appCatalogs/teamsApps/{app_id}"}
    resp = requests.post(f"https://graph.microsoft.com/v1.0/teams/{team_id}/installedApps", headers=headers, json=payload)
    print("Install status:", resp.status_code, resp.text)

if __name__ == "__main__":
    run()
