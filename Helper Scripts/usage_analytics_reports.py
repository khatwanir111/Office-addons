import requests
from helper_auth import get_token

token = get_token()
headers = {"Authorization": f"Bearer {token}"}

# SharePoint usage report
resp = requests.get(
    "https://graph.microsoft.com/v1.0/reports/getSharePointSiteUsageFileCounts(period='D7')",
    headers=headers
)

if resp.ok:
    requests.put(
        "https://graph.microsoft.com/v1.0/me/drive/root:/sharepoint_usage.csv:/content",
        headers={"Authorization": f"Bearer {token}"},
        data=resp.content
    )
    print("Saved usage report.")
else:
    print(resp.status_code, resp.text)
