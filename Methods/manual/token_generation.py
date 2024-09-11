import requests
from keys import keys

def get_token():
    url = "https://exbo.net/oauth/token"
    data = {
        "client_id": f"{keys.client_id}",  
        "client_secret": f"{keys.secret}",  
        "grant_type": "client_credentials",
        "scope": "" 
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        token = response.json().get("access_token")
        return token
    else:
        print(f"Error: {response.status_code}, {response.text}")
