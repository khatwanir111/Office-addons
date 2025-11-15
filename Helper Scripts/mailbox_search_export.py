# mailbox_search_export.py
import os, requests
from helper_auth import get_token

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# 1) Search messages from last 7 days with subject containing "invoice"
query = "receivedDateTime ge {}".format((__import__("datetime").datetime.utcnow() - __import__("datetime").timedelta(days=7)).isoformat()+"Z")
url = f"https://graph.microsoft.com/v1.0/me/messages?$filter=contains(subject,'invoice') and {query}&$top=10"
resp = requests.get(url, headers=headers)
msgs = resp.json().get("value", [])

for i, m in enumerate(msgs):
    # fetch MIME content
    mime = requests.get(f"https://graph.microsoft.com/v1.0/me/messages/{m['id']}/$value", headers={"Authorization": f"Bearer {token}"})
    filename = f"exported_message_{i}.eml"
    # upload to OneDrive
    requests.put(f"https://graph.microsoft.com/v1.0/me/drive/root:/{filename}:/content", headers={"Authorization": f"Bearer {token}"}, data=mime.content)

print("Exported", len(msgs), "messages to OneDrive.")
