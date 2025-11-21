# create_share_link_and_save.py
# ENV: ITEM_PATH (OneDrive path to file, e.g. "/Reports/report.pdf")
import os, requests, json
from helper_auth import get_token

def run():
    item_path = os.environ.get("ITEM_PATH")
    if not item_path:
        print("Set ITEM_PATH in env"); return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    # create a view link (type=view, scope=anonymous or org)
    payload = {"type":"view", "scope":"organization"}  # or "anonymous"
    resp = requests.post(f"https://graph.microsoft.com/v1.0/me/drive/root:{item_path}:/createLink", headers=headers, json=payload)
    if not resp.ok:
        print("Failed to create link:", resp.status_code, resp.text); return
    link = resp.json().get("link", {}).get("webUrl")
    if not link:
        print("No link returned"); return

    # save link text to OneDrive as a small file
    file_name = f"{os.path.basename(item_path)}.sharelink.txt"
    requests.put(f"https://graph.microsoft.com/v1.0/me/drive/root:/{file_name}:/content", headers={**headers, "Content-Type":"text/plain"}, data=link.encode("utf-8"))
    print("Saved sharing link to", file_name)

if __name__ == "__main__":
    run()
