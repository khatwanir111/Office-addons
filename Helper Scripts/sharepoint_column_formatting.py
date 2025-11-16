import os, requests, json
from helper_auth import get_token

def apply_format(site_id, list_id, column_name, formatting_json):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    cols = requests.get(
        f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_id}/columns",
        headers=headers
    ).json().get("value", [])

    col = next((c for c in cols if c["name"] == column_name), None)
    if not col:
        print("Column not found.")
        return

    col_id = col["id"]
    payload = {"format": {"json": formatting_json}}

    resp = requests.patch(
        f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_id}/columns/{col_id}",
        headers=headers, json=payload
    )
    print(resp.status_code, resp.text)
