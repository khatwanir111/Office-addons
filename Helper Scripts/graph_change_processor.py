# graph_change_processor.py
import json, requests
from helper_auth import get_token

def process_notification(notification_json):
    """
    Example processor for a Graph change notification.
    Expects a dict matching Graph notifications (value = [ { resource, subscriptionId, etc } ])
    """
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    for n in notification_json.get("value", []):
        resource = n.get("resource")
        print("Notification for resource:", resource)
        # fetch the resource snapshot from Graph (best-effort)
        fetch_url = f"https://graph.microsoft.com/v1.0{resource}"
        r = requests.get(fetch_url, headers=headers)
        if r.ok:
            snapshot = r.json()
            filename = f"notification_snapshot_{n.get('subscriptionId')}_{n.get('resource').replace('/','_')}.json"
            # upload snapshot to OneDrive
            requests.put(f"https://graph.microsoft.com/v1.0/me/drive/root:/{filename}:/content",
                         headers={**headers, "Content-Type": "application/json"},
                         data=json.dumps(snapshot))
            print("Saved snapshot to OneDrive:", filename)
        else:
            print("Failed to fetch resource:", r.status_code, r.text)


if __name__ == "__main__":
    # demo sample notification
    sample = {"value": [{"subscriptionId": "sample-sub", "resource": "/me/drive/root"}]}
    process_notification(sample)
