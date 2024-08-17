import requests
from api_key import user_id, secret, client_token

def retrieve_login():

    # API endpoint
    url = 'https://eapi.stalcraft.net/EU/character/by-name/Sitrezix/profile'

    # Set up the headers with the OAuth token
    headers = {
        'Authorization': f'Bearer {client_token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
    
        lastLogin = response.json().get("lastLogin")
        print(lastLogin)

        return lastLogin
        
    else:
        print(f"Response content: {response.text}")
