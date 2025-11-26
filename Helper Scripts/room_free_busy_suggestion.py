# room_free_busy_suggestion.py
# ENV: ROOMS (comma-separated SMTP addresses of room mailboxes)
import os, requests, json
from datetime import datetime, timedelta
from helper_auth import get_token

def run():
    rooms = [r.strip() for r in os.environ.get("ROOMS", "").split(",") if r.strip()]
    if not rooms:
        print("Set ROOMS with room mailbox addresses")
        return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    start = datetime.utcnow() + timedelta(hours=1)
    end = start + timedelta(hours=1)
    payload = {
        "schedules": rooms,
        "startTime": {"dateTime": start.isoformat(), "timeZone": "UTC"},
        "endTime": {"dateTime": end.isoformat(), "timeZone": "UTC"},
        "availabilityViewInterval": 30
    }
    resp = requests.post("https://graph.microsoft.com/v1.0/me/calendar/getSchedule", headers=headers, json=payload)
    if not resp.ok:
        print("getSchedule failed:", resp.status_code, resp.text)
        return

    data = resp.json()
    free_rooms = []
    for sched in data.get("value", []):
        if sched.get("availabilityView", "").strip("0") == "":
            free_rooms.append(sched.get("scheduleId"))

    suggestion = {
        "timeWindowStart": start.isoformat() + "Z",
        "timeWindowEnd": end.isoformat() + "Z",
        "freeRooms": free_rooms
    }

    # Save to OneDrive
    put = requests.put(
        "https://graph.microsoft.com/v1.0/me/drive/root:/room_suggestions.json:/content",
        headers={**headers, "Content-Type": "application/json"},
        data=json.dumps(suggestion).encode("utf-8")
    )
    print("Saved room_suggestions.json:", put.status_code, "Free rooms:", free_rooms)

if __name__ == "__main__":
    run()
