import os
import db_key
import api_key


class keys():
    def __init__(self) -> None:
        self.client_id = ""
        self.secret = ""
        self.client_token = ""
        self.user_token = ""
        self.refresh_token = ""
        self.discord_key = ""
        self.user_code = ""
        self.host = ""
        self.dbname = ""
        self.user = ""
        self.port = ""
        self.password = ""
    
    def load_env_keys(self):
        self.client_id = os.getenv('client_id')
        self.secret = os.getenv('secret')
        self.client_token = os.getenv('client_token')
        self.user_token = os.getenv('user_token')
        self. refresh_token = os.getenv('refresh_token')
        self.discord_key = os.getenv('discord_key')
        self.user_code = os.getenv('user_code')
        self.host = os.getenv('host')
        self.dbname = os.getenv('dbname')
        self.user = os.getenv('user')
        self.port = os.getenv('port')
        self.password = os.getenv('password')

    def load_loc_keys(self):
        self.client_id = api_key.client_id
        self.secret = api_key.secret
        self.client_token = api_key.client_token
        self.user_token = api_key.user_code
        self.refresh_token = api_key.refresh_token
        self.discord_key = api_key.discord_key_test
        self.user_code = api_key.user_code
        self.host = db_key.host
        self.dbname = db_key.dbname
        self.user = db_key.user
        self.port = db_key.port
        self.password = db_key.password

    def test(self):
        print(self.client_id)
