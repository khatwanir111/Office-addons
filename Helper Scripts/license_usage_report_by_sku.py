# license_usage_report_by_sku.py
# ENV: none
import os, requests, json
from helper_auth import get_token

def run():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    # list subscribedSkus
    r = requests.get("https://graph.microsoft.com/v1.0/subscribedSkus", headers=headers)
    if not r.ok:
        print("Failed to list SKUs", r.status_code, r.text); return
    skus = r.json().get("value", [])
    report = []
    for sku in skus:
        sku_id = sku.get("skuId")
        sku_part = sku.get("skuPartNumber")
        assigned = sku.get("prepaidUnits", {})
        report.append({"skuId": sku_id, "skuPartNumber": sku_part, "assigned": assigned})
    put = requests.put("https://graph.microsoft.com/v1.0/me/drive/root:/license_usage_report.json:/content",
                       headers={**headers, "Content-Type": "application/json"}, data=json.dumps(report).encode("utf-8"))
    print("Saved license report:", put.status_code)

if __name__ == "__main__":
    run()
