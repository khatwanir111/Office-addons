# onenote_create_section_and_page.py
# ENV: NOTEBOOK_ID (optional – if not set, uses default)
import os, requests
from helper_auth import get_token

def run():
    token = get_token()
    headers_json = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Find notebook
    nb_id = os.environ.get("NOTEBOOK_ID")
    if not nb_id:
        nbs = requests.get("https://graph.microsoft.com/v1.0/me/onenote/notebooks", headers=headers_json).json().get("value", [])
        if not nbs:
            print("No notebooks found")
            return
        nb_id = nbs[0]["id"]

    # Create section
    sec_payload = {"displayName": "Auto Dev Section"}
    sec_resp = requests.post(f"https://graph.microsoft.com/v1.0/me/onenote/notebooks/{nb_id}/sections", headers=headers_json, json=sec_payload)
    if not sec_resp.ok:
        print("Section create failed:", sec_resp.status_code, sec_resp.text)
        return
    sec_id = sec_resp.json()["id"]

    # Create page with HTML
    headers_multipart = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/xhtml+xml"
    }
    html = """
<!DOCTYPE html>
<html>
  <head><title>Dev Page</title></head>
  <body>
    <h1>Automated Dev Page</h1>
    <p>This OneNote page was created by a script.</p>
  </body>
</html>
"""
    page_resp = requests.post(
        f"https://graph.microsoft.com/v1.0/me/onenote/sections/{sec_id}/pages",
        headers=headers_multipart,
        data=html.encode("utf-8")
    )
    print("Page create status:", page_resp.status_code, page_resp.text)

if __name__ == "__main__":
    run()
