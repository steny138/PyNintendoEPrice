import os
import pytest
import logging
from dotenv import load_dotenv
from ns_web_api.music.music_client_factory import MusicClientFactory

logging.basicConfig(level=logging.DEBUG)


class TestSpotifyUserApi:

    def setup_class(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(dotenv_path, override=True)

        factory = MusicClientFactory()
        config = {
            'SPOTIFY_CLIENT_ID': os.getenv('SPOTIFY_CLIENT_ID', ''),
            'SPOTIFY_CLIENT_SECRET': os.getenv('SPOTIFY_CLIENT_SECRET', ''),
            'SPOTIFY_AUTH_REDIRECT_URI': os.getenv('SPOTIFY_AUTH_REDIRECT_URI', ''),
            'YOUTUBE_API_KEY': os.getenv('YOUTUBE_API_KEY', '')
        }

        token = {
            'access_token': os.getenv('SPOTIFY_ACCESS_TOKEN', ''),
            'token_type': 'Bearer',
            'expires_in': 3600,
            'refresh_token': os.getenv('SPOTIFY_REFRESH_TOKEN', ''),
            'scope': ['playlist-modify-public'],
            'expires_at': 1637638561.311397}

        self.sut = factory.spotify_user_client(config, token)
        self.sut_auth = factory.spotify_oauth_client(config)

    @pytest.mark.skip(reason="skip auth tests")
    def test_spotify_api_current_user(self):
        user_id = os.getenv('SPOTIFY_USER', '')

        user = self.sut.current_user(user_id)

        assert user

    def test_spotify_api_create_playlist(self):

        tracks = [
            {"uri": "spotify:track:55h7vJchibLdUkxdlX3fK7"},
            {"uri": "spotify:track:7dQGDSVjt1vS6BsDURjYhS"},
            {"uri": "spotify:track:5k58Fbi1th2ITcaweRSbVq"},
            {"uri": "spotify:track:1vvK3Ey7LxgAFidEmU3QvC"},
            {"uri": "spotify:track:7cHZIHlewdmRCBmuOn4ssV"}
        ]

        playlist = self.sut.create_playlist(
            self.user, "GO API DEMO", tracks=tracks)

        assert playlist

    @pytest.mark.skip(reason="skip auth tests")
    def test_spotify_api_auth(self):

        access_token = self.sut_auth.offline_auth()

        print(access_token)
        assert access_token
