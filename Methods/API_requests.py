import requests
from api_key import user_id, secret, client_token

def retrieve_login(user):

    # API endpoint
    url = f'https://eapi.stalcraft.net/EU/character/by-name/{user}/profile'

    # Set up the headers with the OAuth token
    headers = {
        'Authorization': f'Bearer {client_token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
    
        lastLogin = response.json().get("lastLogin")

        return lastLogin
        
    else:
        error = "Игрок не найден"

        return error