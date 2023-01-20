import requests
import json
import pandas as pd

server_name = "prod-ca-a.online.tableau.com"
api_version = "3.17"
site_url_id = "JasonTesttest"

personal_access_token_name = "TestToken"
personal_access_token_secret = "your password here"

signin_url = f"https://{server_name}/api/{api_version}/auth/signin"
payload = { "credentials": { "personalAccessTokenName": personal_access_token_name, "personalAccessTokenSecret": personal_access_token_secret, "site": {"contentUrl": site_url_id }}}
headers = {
    'accept': 'application/json',
    'content-type': 'application/json'
}

req = requests.post(signin_url, json=payload, headers=headers, verify=False)

response = json.loads(req.content)


site_id = response["credentials"]["site"]["id"]

headers['X-tableau-auth'] = response["credentials"]["token"]
query = """
query datasources {
  datasources {
    name
    id
createdAt
  }
}
"""

url = f'https://{server_name}/relationship-service-war/graphql'
request_body = {'query': query}

response = requests.post(url, headers=headers, json=request_body, verify=False)
data = json.loads(response.content)

df = pd.DataFrame(data["data"]["datasources"])


return df.to_dict(orient='list')