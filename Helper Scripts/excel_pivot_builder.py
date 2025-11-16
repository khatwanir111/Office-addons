import os, requests, json
from helper_auth import get_token

def create_pivot():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Create workbook
    resp = requests.put(
        "https://graph.microsoft.com/v1.0/me/drive/root:/DevPivotDemo.xlsx:/content",
        headers={"Authorization": f"Bearer {token}"}
    )
    file_id = resp.json()["id"]

    # Insert data
    data = {
        "values": [
            ["Category", "Product", "Sales"],
            ["A", "P1", 100],
            ["A", "P2", 200],
            ["B", "P3", 150],
            ["B", "P4", 250],
        ]
    }

    requests.patch(
        f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/workbook/worksheets/Sheet1/range(address='A1:C5')",
        headers=headers, json=data
    )

    # Add table
    table_payload = {"address": "A1:C5", "hasHeaders": True}
    table_resp = requests.post(
        f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/workbook/worksheets/Sheet1/tables/add",
        headers=headers, json=table_payload
    )

    # Add pivot (API limited — demonstration)
    pivot_payload = {
        "name": "PivotSales",
        "source": {"worksheet": "Sheet1", "address": "A1:C5"},
        "rows": [{"sourceName": "Category"}],
        "values": [{"sourceName": "Sales", "aggregation": "sum"}],
    }

    pt_resp = requests.post(
        f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/workbook/worksheets/Sheet1/pivotTables/add",
        headers=headers, json=pivot_payload
    )
    print(pt_resp.status_code, pt_resp.text)


if __name__ == "__main__":
    create_pivot()
