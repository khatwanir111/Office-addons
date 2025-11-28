# org_search_people.py
# ENV: SEARCH_QUERY (e.g. "security", "product manager")
import os, json, requests
from helper_auth import get_token

def run():
    query = os.environ.get("SEARCH_QUERY", "security")
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    payload = {
        "requests": [
            {
                "entityTypes": ["person"],
                "query": {"queryString": query},
                "from": 0,
                "size": 25
            }
        ]
    }

    resp = requests.post("https://graph.microsoft.com/v1.0/search/query", headers=headers, json=payload)
    if not resp.ok:
        print("Search failed:", resp.status_code, resp.text)
        return

    result = resp.json()
    out_name = f"people_search_{query.replace(' ','_')}.json"
    put = requests.put(
        f"https://graph.microsoft.com/v1.0/me/drive/root:/{out_name}:/content",
        headers={"Authorization": f"Bearer {token}", "Content-Type":"application/json"},
        data=json.dumps(result).encode("utf-8")
    )
    print("Saved search results:", put.status_code, "->", out_name)

if __name__ == "__main__":
    run()
