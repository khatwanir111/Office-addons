# generate_html_directory_from_graph.py
# ENV: none
import os, requests
from helper_auth import get_token

def run():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    url = "https://graph.microsoft.com/v1.0/users?$select=displayName,mail,userPrincipalName&$top=50"
    users = []
    while url:
        r = requests.get(url, headers=headers)
        if not r.ok:
            print("User fetch failed:", r.status_code, r.text)
            return
        data = r.json()
        users.extend(data.get("value", []))
        url = data.get("@odata.nextLink")

    rows = []
    for u in users:
        name = u.get("displayName")
        mail = u.get("mail") or u.get("userPrincipalName")
        rows.append(f"<tr><td>{name}</td><td>{mail}</td></tr>")

    html = f"""<!DOCTYPE html>
<html>
  <head><title>Directory</title></head>
  <body>
    <h1>Company Directory (Auto-generated)</h1>
    <table border="1" cellpadding="4" cellspacing="0">
      <tr><th>Name</th><th>Email</th></tr>
      {''.join(rows)}
    </table>
  </body>
</html>"""

    put = requests.put(
        "https://graph.microsoft.com/v1.0/me/drive/root:/directory.html:/content",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "text/html"},
        data=html.encode("utf-8")
    )
    print("Saved directory.html:", put.status_code)

if __name__ == "__main__":
    run()
