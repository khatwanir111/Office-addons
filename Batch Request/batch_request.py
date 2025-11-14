# batch_request.py
import requests, json
from helper_auth import get_token

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

batch_payload = {
  "requests": [
    {"id": "1", "method": "GET", "url": "/me?$select=displayName,mail"},
    {"id": "2", "method": "GET", "url": "/me/drive/root/children?$top=5"},
    {"id": "3", "method": "GET", "url": "/me/joinedTeams"}
  ]
}

resp = requests.post("https://graph.microsoft.com/v1.0/$batch", headers=headers, json=batch_payload)
print(resp.status_code)
print(json.dumps(resp.json(), indent=2))
