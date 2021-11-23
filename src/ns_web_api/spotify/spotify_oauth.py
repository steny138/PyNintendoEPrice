from requests_oauthlib import OAuth2Session


class SpotifyOAuth2:
    def __init__(self, client_id, client_secret) -> None:
        self.auth_domain = "https://accounts.spotify.com"
        self.client_id = client_id
        self.client_secret = client_secret

    def offline_auth(self):
        authorization_url, state = self.authorize()

        print(authorization_url, state)

        response_url = input(
            "please input redirect response url from authorization_url: \n")

        token = self.get_token(response_url, state)

        self.token = token

        return token

    def authorize(self):
        oauth = self.__create_session()

        authorization_url, state = oauth.authorization_url(
            f'{self.auth_domain}/authorize',
            access_type="offline",
            prompt="select_account")

        return authorization_url, state

    def get_token(self, response_url, state):
        oauth = self.__create_session(state)

        token = oauth.fetch_token(
            f'{self.auth_domain}/api/token',
            authorization_response=response_url,
            client_secret=self.client_secret)

        return token

    def __create_session(self, state=None):

        # Note that these are Google specific scopes
        scope = ['playlist-modify-public']

        redirect_uri = "https://3e48-211-23-179-226.ngrok.io/oauth2/callback"

        oauth = OAuth2Session(self.client_id,
                              redirect_uri=redirect_uri,
                              scope=scope,
                              state=state)

        return oauth
