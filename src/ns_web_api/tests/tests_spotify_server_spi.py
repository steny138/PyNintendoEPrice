from ns_web_api.music.music_client_factory import MusicClientFactory
from dotenv import load_dotenv
import os


class TestSpotifyServerApi:

    def setup_class(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(dotenv_path, override=True)
        factory = MusicClientFactory()
        config = {
            'SPOTIFY_CLIENT_ID': os.getenv('SPOTIFY_CLIENT_ID', ''),
            'SPOTIFY_CLIENT_SECRET': os.getenv('SPOTIFY_CLIENT_SECRET', ''),
            'SPOTIFY_AUTH_REDIRECT_URI': os.getenv('SPOTIFY_AUTH_REDIRECT_URI', ''),
            'YOUTUBE_API_KEY': os.getenv('YOUTUBE_API_KEY', '')}

        token = {
            'access_token': os.getenv('SPOTIFY_ACCESS_TOKEN', ''),
            'token_type': 'Bearer',
            'expires_in': 3600,
            'refresh_token': os.getenv('SPOTIFY_REFRESH_TOKEN', ''),
            'scope': ['playlist-modify-public'],
            'expires_at': 1637638561.311397}

        self.sut = factory.spotify_server_client(config)

    def test_spotify_auth_client_credentials(self):
        actual = self.sut.auth_client_redentials()

        assert actual

    def tests_query(self):
        query = "Bruno Mars - Treasure"

        actual = self.sut.query(query)

        assert actual
