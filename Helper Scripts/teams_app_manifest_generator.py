import json, os
from datetime import datetime

manifest = {
    "$schema": "https://developer.microsoft.com/en-us/json-schemas/teams/v1.11/MicrosoftTeams.schema.json",
    "manifestVersion": "1.11",
    "id": os.environ.get("TEAMS_APP_ID", "00000000-0000-0000-0000-000000000000"),
    "version": "1.0.0",
    "packageName": f"com.example.auto.{int(datetime.utcnow().timestamp())}",
    "developer": {
        "name": "Automated Dev",
        "websiteUrl": "https://example.com",
        "privacyUrl": "https://example.com/privacy",
        "termsOfUseUrl": "https://example.com/terms"
    },
    "name": {"short": "AutoApp", "full": "Automated Teams App"},
    "description": {"short": "Auto App", "full": "Teams app generated automatically"},
    "icons": {"outline": "outline.png", "color": "color.png"},
    "accentColor": "#FFFFFF",
    "staticTabs": [],
    "bots": [],
    "permissions": ["identity"],
    "validDomains": []
}

os.makedirs("teams_app", exist_ok=True)
with open("teams_app/manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

print("Created teams_app/manifest.json")
