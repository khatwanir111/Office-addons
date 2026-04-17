import requests

ACCESS_TOKEN = "your-access-token"

USER_IDS = [
    "user-id-1",
    "user-id-2"
]

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def disable_user(user_id):
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}"

    payload = {"accountEnabled": False}

    response = requests.patch(url, headers=headers, json=payload)

    if response.status_code == 204:
        print(f"{user_id} disabled")
    else:
        print(f"Failed for {user_id}")

if __name__ == "__main__":
    for uid in USER_IDS:
        disable_user(uid)
