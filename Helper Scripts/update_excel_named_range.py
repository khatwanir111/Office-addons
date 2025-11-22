# update_excel_named_range.py
# ENV: FILE_ITEM_ID (OneDrive item id) or FILE_PATH (e.g., /Config/config.xlsx), NAMED_RANGE, NEW_VALUES_JSON (e.g., '[[1,2],[3,4]]')
import os, requests, json
from helper_auth import get_token

def run():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    file_path = os.environ.get("FILE_PATH")
    item_id = os.environ.get("FILE_ITEM_ID")
    named = os.environ.get("NAMED_RANGE")
    new_values = json.loads(os.environ.get("NEW_VALUES_JSON", "[]"))

    if not (named and (file_path or item_id)):
        print("Set NAMED_RANGE and FILE_PATH or FILE_ITEM_ID"); return

    if not item_id:
        # resolve to item id
        r = requests.get(f"https://graph.microsoft.com/v1.0/me/drive/root:{file_path}", headers=headers)
        if not r.ok:
            print("Failed to resolve file path"); return
        item_id = r.json()["id"]

    # write values to named range
    payload = {"values": new_values}
    resp = requests.patch(f"https://graph.microsoft.com/v1.0/me/drive/items/{item_id}/workbook/names/{named}/range", headers=headers, json=payload)
    # If not supported, fallback to writing by address returned from name
    if resp.status_code in (200,204):
        print("Updated named range")
    else:
        # try get named range address then update range
        info = requests.get(f"https://graph.microsoft.com/v1.0/me/drive/items/{item_id}/workbook/names/{named}", headers=headers)
        if info.ok:
            addr = info.json().get("workbookRangeAddress")
            if addr:
                r2 = requests.patch(f"https://graph.microsoft.com/v1.0/me/drive/items/{item_id}/workbook/worksheets('{addr.split('!')[0]}')/range(address='{addr.split('!')[1]}')",
                                     headers=headers, json={"values": new_values})
                print("Fallback update status:", r2.status_code, r2.text)
        else:
            print("Update failed:", resp.status_code, resp.text)

if __name__ == "__main__":
    run()
