import requests
import time

ACCESS_TOKEN = "your-access-token"
TEAM_ID = "your-team-id"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

def archive_team():
    url = f"https://graph.microsoft.com/v1.0/teams/{TEAM_ID}/archive"
    response = requests.post(url, headers=headers)

    if response.status_code == 202:
        print("Team archived")

def unarchive_team():
    url = f"https://graph.microsoft.com/v1.0/teams/{TEAM_ID}/unarchive"
    response = requests.post(url, headers=headers)

    if response.status_code == 202:
        print("Team unarchived")

if __name__ == "__main__":
    archive_team()
    time.sleep(5)
    unarchive_team()
