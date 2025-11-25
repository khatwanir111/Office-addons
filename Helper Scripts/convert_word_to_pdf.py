# convert_word_to_pdf.py
# ENV: SOURCE_PATH (OneDrive path) e.g. "/Docs/doc.docx"
#      DEST_PATH (OneDrive path) e.g. "/Docs/doc.pdf"
import os, requests
from helper_auth import get_token

def run():
    source = os.environ.get("SOURCE_PATH")
    dest = os.environ.get("DEST_PATH", (source or "").rsplit(".",1)[0] + ".pdf" if source else None)
    if not source or not dest:
        print("Set SOURCE_PATH and optionally DEST_PATH"); return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Download as PDF using format query parameter
    url = f"https://graph.microsoft.com/v1.0/me/drive/root:{source}:/content?format=pdf"
    r = requests.get(url, headers=headers)
    if not r.ok:
        print("Conversion/download failed:", r.status_code, r.text); return

    # Upload PDF to OneDrive
    put = requests.put(f"https://graph.microsoft.com/v1.0/me/drive/root:{dest}:/content", headers={**headers, "Content-Type":"application/pdf"}, data=r.content)
    print("Saved PDF:", put.status_code, put.text)

if __name__ == "__main__":
    run()
