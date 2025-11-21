# invite_guest_user.py
# ENV: GUEST_EMAIL, INVITE_REDIRECT_URL (optional)
import os, requests
from helper_auth import get_token

def run():
    guest = os.environ.get("GUEST_EMAIL")
    redirect = os.environ.get("INVITE_REDIRECT_URL", "https://myapp.example.com")
    if not guest:
        print("Set GUEST_EMAIL in env"); return

    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    payload = {
      "invitedUserEmailAddress": guest,
      "inviteRedirectUrl": redirect,
      "sendInvitationMessage": True,
      "invitedUserMessageInfo": {"customizedMessageBody": "Please join our tenant for testing."}
    }

    resp = requests.post("https://graph.microsoft.com/v1.0/invitations", headers=headers, json=payload)
    if resp.ok:
        print("Invitation created:", resp.json().get("id"))
    else:
        print("Failed to invite:", resp.status_code, resp.text)

if __name__ == "__main__":
    run()
