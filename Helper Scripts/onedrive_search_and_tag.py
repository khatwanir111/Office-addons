import os, requests, json
from helper_auth import get_token

def tag_files(term="report"):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    resp = requests.get(
        f"https://graph.microsoft.com/v1.0/me/drive/root/search(q='{term}')",
        headers=headers
    )
    items = resp.json().get("value", [])

    for item in items:
        name = item["name"]
        tags = {"autoTags": ["generated", term]}

        requests.put(
            f"https://graph.microsoft.com/v1.0/me/drive/root:/{name}.tags.json:/content",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            data=json.dumps(tags)
        )
        print("Tagged:", name)


if __name__ == "__main__":
    tag_files()
