import hmac
import hashlib
import base64
import os
import json

def validate_webhook(req_body: bytes, headers: dict) -> bool:
    expected_client_state = os.environ.get("SUBSCRIPTION_CLIENT_STATE", "secret-opaque-value")

    try:
        body = json.loads(req_body.decode("utf-8"))
    except:
        return False

    if "validationToken" in body:
        print("Validation token:", body["validationToken"])
        return True

    for n in body.get("value", []):
        if n.get("clientState") != expected_client_state:
            print("clientState mismatch")
            return False

    sig_header = headers.get("x-ms-signature") or headers.get("X-MS-Signature")
    shared_secret = os.environ.get("WEBHOOK_SHARED_SECRET")

    if sig_header and shared_secret:
        expected = base64.b64encode(
            hmac.new(shared_secret.encode(), req_body, hashlib.sha256).digest()
        ).decode()
        if not hmac.compare_digest(expected, sig_header):
            print("HMAC mismatch")
            return False

    print("Webhook validated.")
    return True
