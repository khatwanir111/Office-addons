# calendar_to_sheet.py
# ENV: DAYS (optional, default 7)
import os, requests, json
from datetime import datetime, timedelta
from helper_auth import get_token

def run():
    days = int(os.environ.get("DAYS", "7"))
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    start = datetime.utcnow().isoformat() + "Z"
    end = (datetime.utcnow() + timedelta(days=days)).isoformat() + "Z"
    q = f"https://graph.microsoft.com/v1.0/me/calendarview?startdatetime={start}&enddatetime={end}&$top=100"
    r = requests.get(q, headers=headers)
    if not r.ok:
        print("Calendar fetch failed", r.status_code, r.text); return
    events = r.json().get("value", [])

    # Build table values
    values = [["subject","start","end","organizer","location"]]
    for e in events:
        values.append([
            e.get("subject"),
            e.get("start",{}).get("dateTime"),
            e.get("end",{}).get("dateTime"),
            e.get("organizer",{}).get("emailAddress",{}).get("name"),
            e.get("location",{}).get("displayName")
        ])

    # create workbook and write range
    resp = requests.put("https://graph.microsoft.com/v1.0/me/drive/root:/calendar_export.xlsx:/content",
                        headers={**headers}, data=b"")
    if not resp.ok:
        print("Create workbook failed", resp.status_code, resp.text); return
    file_id = resp.json()["id"]
    patch = requests.patch(f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/workbook/worksheets/Sheet1/range(address='A1:E{len(values)}')",
                           headers=headers, json={"values": values})
    print("Wrote calendar to workbook:", patch.status_code)

if __name__ == "__main__":
    run()
