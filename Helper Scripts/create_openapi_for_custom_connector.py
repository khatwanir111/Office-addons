# create_openapi_for_custom_connector.py
import os, json, requests
from helper_auth import get_token

def run():
    openapi = {
      "openapi": "3.0.1",
      "info": {"title": "Auto Connector", "version": "1.0.0"},
      "paths": {
        "/hello": {
          "get": {
            "summary": "Say hello",
            "responses": {"200": {"description": "OK", "content": {"application/json": {"schema": {"type":"object"}}}}}
          }
        }
      },
      "servers": [{"url":"https://example.com/api"}]
    }
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}
    put = requests.put("https://graph.microsoft.com/v1.0/me/drive/root:/custom_connector_openapi.json:/content",
                       headers=headers, data=json.dumps(openapi).encode("utf-8"))
    print("Saved openapi file:", put.status_code)

if __name__ == "__main__":
    run()
