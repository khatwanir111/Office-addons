import requests

ACCESS_TOKEN = "your-access-token"
GROUP_ID = "your-group-id"

USER_IDS = [
    "user-id-1",
    "user-id-2"
]

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def add_user(user_id):
    url = f"https://graph.microsoft.com/v1.0/groups/{GROUP_ID}/members/$ref"

    payload = {
        "@odata.id": f"https://graph.microsoft.com/v1.0/directoryObjects/{user_id}"
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 204:
        print(f"Added {user_id}")
    else:
        print(f"Failed {user_id}: {response.text}")

if __name__ == "__main__":
    for uid in USER_IDS:
        add_user(uid)
