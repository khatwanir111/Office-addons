# sharepoint_termstore_create_terms.py
# ENV: TERMSET_NAME (e.g. "ProjectCategories"), TERMS (comma-separated)
import os, requests
from uuid import uuid4
from helper_auth import get_token

def run():
    termset_name = os.environ.get("TERMSET_NAME", "AutoTermSet")
    terms = [t.strip() for t in os.environ.get("TERMS", "Alpha,Beta,Gamma").split(",") if t.strip()]

    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}

    # Get default termStore
    store = requests.get("https://graph.microsoft.com/v1.0/sites/root/termStore", headers=headers)
    if not store.ok:
        print("Term store fetch failed:", store.status_code, store.text)
        return
    store_id = store.json()["id"]

    # Create term set
    ts_payload = {"id": str(uuid4()), "localizedNames":[{"name":termset_name,"languageTag":"en-US"}]}
    ts_resp = requests.post(f"https://graph.microsoft.com/v1.0/sites/root/termStore/groups/{store_id}/sets", headers=headers, json=ts_payload)
    if not ts_resp.ok:
        print("Term set create failed:", ts_resp.status_code, ts_resp.text)
        return
    termset_id = ts_resp.json()["id"]

    # Add terms
    for t in terms:
        term_payload = {
            "id": str(uuid4()),
            "labels":[{"name":t,"languageTag":"en-US","isDefault":True}]
        }
        tr = requests.post(f"https://graph.microsoft.com/v1.0/sites/root/termStore/sets/{termset_id}/terms", headers=headers, json=term_payload)
        print("Create term", t, "status:", tr.status_code)

if __name__ == "__main__":
    run()
