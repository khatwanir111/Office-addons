# create_drive_upload_session.py
# ENV: LOCAL_FILE_PATH (local runner), DEST_PATH (OneDrive path, e.g. "/LargeUploads/big.bin")
import os, requests
from helper_auth import get_token

def run():
    local = os.environ.get("LOCAL_FILE_PATH", "large_dummy.bin")
    dest = os.environ.get("DEST_PATH", "/LargeUploads/large_dummy.bin")
    if not os.path.exists(local):
        # create a small dummy if missing
        with open(local, "wb") as f:
            f.write(b"0" * 1024 * 50)  # 50KB dummy
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    # create upload session
    sess_resp = requests.post(f"https://graph.microsoft.com/v1.0/me/drive/root:{dest}:/createUploadSession", headers=headers, json={"item": {"@microsoft.graph.conflictBehavior": "replace"}})
    if not sess_resp.ok:
        print("Failed to create upload session:", sess_resp.status_code, sess_resp.text); return
    upload_url = sess_resp.json().get("uploadUrl")
    # read file and upload in a single chunk (for demo; for large files, chunk appropriately)
    with open(local, "rb") as f:
        data = f.read()
    put = requests.put(upload_url, headers={"Content-Range": f"bytes 0-{len(data)-1}/{len(data)}", "Content-Length": str(len(data))}, data=data)
    print("Upload status:", put.status_code, put.text)

if __name__ == "__main__":
    run()
