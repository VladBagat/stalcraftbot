import requests
from Methods.api_key import client_id, secret, client_token

def get_token():
    url = "https://exbo.net/oauth/token"
    data = {
        "client_id": f"{client_id}",  
        "client_secret": f"{secret}",  
        "grant_type": "client_credentials",
        "scope": "" 
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        token = response.json().get("access_token")
        return token
    else:
        print(f"Error: {response.status_code}, {response.text}")
