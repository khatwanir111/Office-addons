# verify_file_checksum_after_copy.py
# ENV: FILE_PATH (OneDrive path), CHECKSUM_FILE_PATH (optional path to file with expected checksum)
import os, requests, hashlib
from helper_auth import get_token

def run():
    file_path = os.environ.get("FILE_PATH")
    checksum_path = os.environ.get("CHECKSUM_FILE_PATH")
    if not file_path:
        print("Set FILE_PATH in env"); return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    r = requests.get(f"https://graph.microsoft.com/v1.0/me/drive/root:{file_path}:/content", headers=headers)
    if not r.ok:
        print("Failed to download file", r.status_code, r.text); return
    data = r.content
    sha256 = hashlib.sha256(data).hexdigest()
    print("Computed SHA256:", sha256)

    expected = None
    if checksum_path:
        c = requests.get(f"https://graph.microsoft.com/v1.0/me/drive/root:{checksum_path}:/content", headers=headers)
        if c.ok:
            expected = c.content.decode().strip()
            print("Expected checksum:", expected)
    if expected:
        print("Match:", expected.lower() == sha256.lower())
    else:
        # save computed checksum to OneDrive next to file
        name = os.path.basename(file_path)
        put_name = f"{name}.sha256"
        requests.put(f"https://graph.microsoft.com/v1.0/me/drive/root:/{put_name}:/content", headers={**headers, "Content-Type":"text/plain"}, data=sha256.encode())
        print("Saved checksum to", put_name)

if __name__ == "__main__":
    run()
