from datetime import datetime

from src.utils.config import get_config_json
from .gather_keys_oauth2 import OAuth2Server


class FitbitAuthenticator:

    def __init__(self, config_file: str):
        config_dict = get_config_json(config_file)

        self.client_id = config_dict['client_id']
        self.client_secret = config_dict['client_secret']
        self.access_token = None
        self.refresh_token = None

    def authenticate_in_browser(self):
        server = OAuth2Server(self.client_id, self.client_secret)
        server.browser_authorize()

        self.access_token = str(server.fitbit.client.session.token['access_token'])
        self.refresh_token = str(server.fitbit.client.session.token['refresh_token'])

        profile = server.fitbit.user_profile_get()
        print('You are authorized to access data for the user: {}'.format(profile['user']['fullName']))
        for key, value in server.fitbit.client.session.token.items():
            if key == 'access_token':
                print('{} = {}'.format(key, value))
            if key == 'expires_at':
                print('{} = {}'.format(key, datetime.fromtimestamp(value)))
