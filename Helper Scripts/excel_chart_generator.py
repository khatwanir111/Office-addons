# excel_chart_generator.py
import requests
from helper_auth import get_token

def create_chart():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Create a workbook
    create = requests.put("https://graph.microsoft.com/v1.0/me/drive/root:/chart_demo.xlsx:/content", headers={"Authorization": f"Bearer {token}"}, data=b"")
    if not create.ok:
        print("Create workbook failed:", create.status_code, create.text); return
    file_id = create.json()["id"]

    # Add data to sheet range
    data = {"values": [["Month", "Sales"], ["Jan", 100], ["Feb", 150], ["Mar", 130]]}
    requests.patch(f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/workbook/worksheets/Sheet1/range(address='A1:B4')",
                   headers=headers, json=data)

    # Add chart (column clustered)
    chart_payload = {"type": "columnClustered", "sourceData": {"sheet": "Sheet1", "address": "A1:B4"}, "name": "SalesChart"}
    chart_resp = requests.post(f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/workbook/worksheets/Sheet1/charts/add", headers=headers, json=chart_payload)
    print("Chart create status:", chart_resp.status_code, chart_resp.text)

if __name__ == "__main__":
    create_chart()
