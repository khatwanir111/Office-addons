# mailbox_folder_counts_report.py
# ENV: none
import os, requests, json
from helper_auth import get_token

def run():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    r = requests.get("https://graph.microsoft.com/v1.0/me/mailFolders?$top=50", headers=headers)
    if not r.ok:
        print("Failed to list folders", r.status_code, r.text); return
    out = {}
    for f in r.json().get("value", []):
        fid = f.get("id")
        count_resp = requests.get(f"https://graph.microsoft.com/v1.0/me/mailFolders/{fid}?$select=displayName,totalItemCount", headers=headers)
        if count_resp.ok:
            data = count_resp.json()
            out[data["displayName"]] = data.get("totalItemCount", 0)
    put = requests.put("https://graph.microsoft.com/v1.0/me/drive/root:/mailbox_folder_counts.json:/content",
                       headers={**headers, "Content-Type":"application/json"}, data=json.dumps(out).encode("utf-8"))
    print("Saved mailbox_folder_counts.json:", put.status_code)

if __name__ == "__main__":
    run()
