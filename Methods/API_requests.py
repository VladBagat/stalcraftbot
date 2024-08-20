import requests
from api_key import client_id, secret, client_token

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
    

def retrieve_clan_members():

    clan_id = "9d49d17e-8b20-45de-b0d1-6574bcd92a3d"

    #API endpoint
    url = f'https://eapi.stalcraft.net/EU/clan/{clan_id}/info'

    # Set up the headers with the OAuth token
    headers = {
        'Authorization': f'Bearer {client_token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
    
        print(response.json())
        
    else:
        return 
    
retrieve_clan_members()