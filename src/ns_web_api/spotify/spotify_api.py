import requests
from requests_oauthlib import OAuth2Session


class SpotifyApi:

    def __init__(self, client_id, client_secret, token_dict) -> None:
        self.auth_domain = "https://accounts.spotify.com"
        self.domain = "https://api.spotify.com"
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token_dict
        self.session = self.__create_session()

    def create_playlist(self, tracks):
        pass

    def current_user(self, user_id):
        url = f"{self.domain}/v1/users/{user_id}"

        resp = self.session.get(url)

        if resp.status_code == requests.status_codes.codes.ok:
            return resp.text

    def __create_session(self):

        # Note that these are Google specific scopes
        scope = ['playlist-modify-public']

        redirect_uri = "https://3e48-211-23-179-226.ngrok.io/oauth2/callback"

        oauth = OAuth2Session(self.client_id,
                              redirect_uri=redirect_uri,
                              scope=scope,
                              token=self.token)

        return oauth
