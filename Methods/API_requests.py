import requests
from keys import keys

def retrieve_online(user) -> str:

    # API endpoint
    url = f'https://eapi.stalcraft.net/EU/character/by-name/{user}/profile'

    # Set up the headers with the OAuth token
    headers = {
        "Content-Type": "application/json",
        'Authorization': f'Bearer {keys.client_token}'
    }

    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
    
        lastLogin = response.json().get("lastLogin")

        return lastLogin
        
    else:
        raise ValueError('Player not found')
    

def retrieve_clan_members():

    #Og Groove Street id
    clan_id = "9d49d17e-8b20-45de-b0d1-6574bcd92a3d"
    
    url = f'https://eapi.stalcraft.net/EU/clan/{clan_id}/members'

    # Set up the headers with the OAuth token
    headers = {
        "Content-Type": "application/json",
        'Authorization': f'Bearer {keys.user_token}'
    }

    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
    
        return response.json()
        
    else:
        
        return f"Error: {response.status_code}, {response.text}"
    
def parse_clan_members():
    names = []
    ranks = []

    players = retrieve_clan_members()

    for i in range(len(players)):
        names.append(players[i].get("name"))
        ranks.append(players[i].get("rank"))

    return names, ranks
