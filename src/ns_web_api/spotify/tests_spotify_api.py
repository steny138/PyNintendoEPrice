import os
import pytest
from spotify_api import SpotifyApi
from spotify_oauth import SpotifyOAuth2
from dotenv import load_dotenv


class TestSpotifyApi:

    def setup_class(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(dotenv_path, override=True)

        self.client_id = os.getenv('SPOTIFY_CLIENT_ID', '')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET', '')
        self.access_token = os.getenv('SPOTIFY_ACCESS_TOKEN', '')
        self.refresh_token = os.getenv('SPOTIFY_REFRESH_TOKEN', '')

    def test_spotify_api_current_user(self):
        token = {'access_token': self.access_token,
                 'token_type': 'Bearer',
                 'expires_in': 3600,
                 'refresh_token': self.refresh_token,
                 'scope': ['playlist-modify-public'],
                 'expires_at': 1637638561.311397}

        api = SpotifyApi(self.client_id, self.client_secret, token)

        user = api.current_user("steny1127")

        print(user)
        assert user

    @pytest.mark.skip(reason="skip auth tests")
    def test_spotify_api_auth(self):
        api = SpotifyOAuth2(self.client_id, self.client_secret)

        access_token = api.offline_auth()

        print(access_token)

        assert access_token
