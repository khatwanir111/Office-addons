import os
from textwrap import dedent

APP_NAME = os.getenv("M365_APP_NAME", "My M365 Dev App")
API_PERMISSIONS = [
    "User.Read.All (Application)",
    "Sites.ReadWrite.All (Application)",
    "Mail.Send (Application)",
]

OUTPUT_FILE = "APP_REGISTRATION_README.md"

def generate_readme():
    perm_lines = "\n".join(f"- {p}" for p in API_PERMISSIONS)
    content = dedent(f"""
    # {APP_NAME} – Microsoft 365 App Registration

    ## 1. App Registration (Entra ID)
    - Go to Entra ID → App registrations
    - Register a new application named **{APP_NAME}**
    - Set:
      - `Application (client) ID`
      - `Directory (tenant) ID`
      - Client secret

    ## 2. API Permissions (Microsoft Graph)
    Grant the following permissions and **admin consent**:

    {perm_lines}

    ## 3. Environment Variables

    ```bash
    export M365_TENANT_ID="<tenant-id>"
    export M365_CLIENT_ID="<client-id>"
    export M365_CLIENT_SECRET="<client-secret>"
    ```

    ## 4. Notes
    - Use client credentials flow via MSAL.
    - Rotate client secrets regularly.
    """).strip() + "\n"

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"README generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_readme()
