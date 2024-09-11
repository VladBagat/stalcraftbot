import requests
from keys import keys

def get_token():
    url = "https://exbo.net/oauth/token"
    data = {
        "client_id": f"{keys.client_id}",  
        "client_secret": f"{keys.secret}",  
        "code": f"{keys.user_code}",
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

def refresh_token():
    url = "https://exbo.net/oauth/token"
    data = {
        "client_id": f"{keys.client_id}",  
        "client_secret": f"{keys.secret}",  
        "refresh_token": f"{keys.refresh_token}",
        "grant_type": "refresh_token"
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        token = response.json()
        print(token)
        return token
    else:
        print(f"Error: {response.status_code}, {response.text}")