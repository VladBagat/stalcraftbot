import requests
from api_key import user_id, secret

def get_token():
    url = "https://exbo.net/oauth/token"
    data = {
        "client_id": f"{user_id}",  
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
    

token = get_token()

def retrieve_login():

    # API endpoint
    url = 'https://eapi.stalcraft.net/EU/character/by-name/Sitrezix/profile'

    # Set up the headers with the OAuth token
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
    
        lastLogin = response.json().get("lastLogin")
        print(lastLogin)

        return lastLogin
        
    else:
        print(f"Response content: {response.text}")

retrieve_login()