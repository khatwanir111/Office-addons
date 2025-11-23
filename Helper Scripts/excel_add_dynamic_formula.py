# excel_add_dynamic_formula.py
# ENV: FILE_PATH (OneDrive path e.g. /AutoSheet.xlsx) or FILE_ITEM_ID
import os, requests, json
from helper_auth import get_token

def run():
    file_path = os.environ.get("FILE_PATH", "/AutoSheet.xlsx")
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    # create or get file
    resp = requests.put(f"https://graph.microsoft.com/v1.0/me/drive/root:{file_path}:/content", headers={**headers}, data=b"")  # idempotent create
    if not resp.ok:
        print("Failed to create/get file", resp.status_code, resp.text); return
    item_id = resp.json()["id"]

    # write header + 2 value rows
    values = {"values":[["Name","Value","Computed"], ["A",10,"=B2*2"], ["B",25,"=B3*2"]]}
    requests.patch(f"https://graph.microsoft.com/v1.0/me/drive/items/{item_id}/workbook/worksheets/Sheet1/range(address='A1:C3')", headers=headers, json=values)

    # read back range to get computed values (Graph may return formulas or results depending on API)
    read = requests.get(f"https://graph.microsoft.com/v1.0/me/drive/items/{item_id}/workbook/worksheets/Sheet1/range(address='A1:C3')", headers=headers)
    if read.ok:
        print("Range values:", json.dumps(read.json().get("values", []), indent=2))
    else:
        print("Read failed", read.status_code, read.text)

if __name__ == "__main__":
    run()
