
from ns_web_api.music.sporify_api import SpotifyApi
from dotenv import load_dotenv
import os


class TestSpotifyApi:

    def setup_class(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(dotenv_path, override=True)

        self.sut = SpotifyApi(os.getenv('SPOTIFY_CLIENT_ID', ''),
                              os.getenv('SPOTIFY_CLIENT_SECRET', ''))

    def test_spotify_auth_client_credentials(self):
        actual = self.sut.auth_client_redentials()

        assert actual

    def tests_query(self):
        query = "Bruno Mars - Treasure"

        actual = self.sut.query(query)

        print(actual)
        assert actual
