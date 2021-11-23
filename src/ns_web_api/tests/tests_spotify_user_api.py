import os
import pytest
from ns_web_api.music.spotify_user_api import SpotifyUserApi
from ns_web_api.music.spotify_oauth import SpotifyOAuth2
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)


class TestSpotifyUserApi:

    def setup_class(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(dotenv_path, override=True)

        self.client_id = os.getenv('SPOTIFY_CLIENT_ID', '')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET', '')
        self.access_token = os.getenv('SPOTIFY_ACCESS_TOKEN', '')
        self.refresh_token = os.getenv('SPOTIFY_REFRESH_TOKEN', '')
        self.user = os.getenv('SPOTIFY_USER', '')
        self.redirect_uri = os.getenv('SPOTIFY_AUTH_REDIRECT_URI', '')

    @pytest.mark.skip(reason="skip auth tests")
    def test_spotify_api_current_user(self):
        token = {'access_token': self.access_token,
                 'token_type': 'Bearer',
                 'expires_in': 3600,
                 'refresh_token': self.refresh_token,
                 'scope': ['playlist-modify-public'],
                 'expires_at': 1637638561.311397}

        api = SpotifyUserApi(self.client_id,
                             self.client_secret,
                             token,
                             self.redirect_uri)

        user = api.current_user(self.user)

        assert user

    def test_spotify_api_create_playlist(self):
        token = {'access_token': self.access_token,
                 'token_type': 'Bearer',
                 'expires_in': 3600,
                 'refresh_token': self.refresh_token,
                 'scope': ['playlist-modify-public'],
                 'expires_at': 1637683195.175843}

        tracks = [
            {"uri": "spotify:track:55h7vJchibLdUkxdlX3fK7"},
            {"uri": "spotify:track:7dQGDSVjt1vS6BsDURjYhS"},
            {"uri": "spotify:track:5k58Fbi1th2ITcaweRSbVq"},
            {"uri": "spotify:track:1vvK3Ey7LxgAFidEmU3QvC"},
            {"uri": "spotify:track:7cHZIHlewdmRCBmuOn4ssV"}
        ]

        api = SpotifyUserApi(self.client_id,
                             self.client_secret,
                             token,
                             self.redirect_uri)

        playlist = api.create_playlist(self.user, "GO API DEMO", tracks=tracks)

        assert playlist

    @pytest.mark.skip(reason="skip auth tests")
    def test_spotify_api_auth(self):
        api = SpotifyOAuth2(self.client_id,
                            self.client_secret,
                            self.redirect_uri)

        access_token = api.offline_auth()

        print(access_token)
        assert access_token
