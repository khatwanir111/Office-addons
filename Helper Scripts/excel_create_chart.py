# excel_create_chart.py
import os, requests, json
from helper_auth import get_token

def run():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    # create workbook
    r = requests.put("https://graph.microsoft.com/v1.0/me/drive/root:/ChartDemo.xlsx:/content", headers={**headers}, data=b"")
    if not r.ok:
        print("Create workbook failed", r.status_code, r.text); return
    file_id = r.json()["id"]

    # write data in A1:B5
    data = {"values":[["Month","Sales"],["Jan",100],["Feb",120],["Mar",90],["Apr",150]]}
    requests.patch(f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/workbook/worksheets/Sheet1/range(address='A1:B5')", headers=headers, json=data)

    # create chart
    chart_payload = {
        "type": "ColumnClustered",
        "sourceData": {"worksheet": "Sheet1", "address": "A1:B5"},
        "seriesBy": "Columns"
    }
    resp = requests.post(f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/workbook/worksheets/Sheet1/charts/add", headers=headers, json=chart_payload)
    print("Chart create status:", resp.status_code, resp.text)

if __name__ == "__main__":
    run()
