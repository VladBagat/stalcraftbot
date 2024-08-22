import requests
from api_key import client_id, secret, client_token, user_code

def get_token():
    url = "https://exbo.net/oauth/token"
    data = {
        "client_id": f"{client_id}",  
        "client_secret": f"{secret}",  
        "code": f"{user_code}",
        "grant_type": "authorization_code",
        "redirect_uri": "http://ssdimages.rf.gd"

    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        token = response.json()
        print(token)
        return token
    else:
        print(f"Error: {response.status_code}, {response.text}")

