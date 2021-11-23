from ns_web_api.music.sporify_server_api import SpotifyServerApi
from dotenv import load_dotenv
import os


class TestSpotifyServerApi:

    def setup_class(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(dotenv_path, override=True)

        self.sut = SpotifyServerApi(os.getenv('SPOTIFY_CLIENT_ID', ''),
                                    os.getenv('SPOTIFY_CLIENT_SECRET', ''))

    def test_spotify_auth_client_credentials(self):
        actual = self.sut.auth_client_redentials()

        assert actual

    def tests_query(self):
        query = "Bruno Mars - Treasure"

        actual = self.sut.query(query)

        assert actual
