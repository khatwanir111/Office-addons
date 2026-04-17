import requests

ACCESS_TOKEN = "your-access-token"
SEARCH_QUERY = "report"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

def search_docs():
    url = f"https://graph.microsoft.com/v1.0/search/query"

    payload = {
        "requests": [
            {
                "entityTypes": ["driveItem"],
                "query": {"queryString": SEARCH_QUERY}
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    hits = data.get("value", [])[0].get("hitsContainers", [])[0].get("hits", [])

    for hit in hits:
        resource = hit.get("resource", {})
        print(resource.get("name"))

if __name__ == "__main__":
    search_docs()
