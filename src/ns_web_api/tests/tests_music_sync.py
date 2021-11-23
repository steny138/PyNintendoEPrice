from ns_web_api.music.music_sync import MusicSync
from dotenv import load_dotenv
import os


class TestSpotifyServerApi:
    def setup_class(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(dotenv_path, override=True)

        token = {'access_token': os.getenv('SPOTIFY_ACCESS_TOKEN', ''),
                 'token_type': 'Bearer',
                 'expires_in': 3600,
                 'refresh_token': os.getenv('SPOTIFY_REFRESH_TOKEN', ''),
                 'scope': ['playlist-modify-public'],
                 'expires_at': 1637638561.311397}

        self.sut = MusicSync(os.getenv('SPOTIFY_CLIENT_ID', ''),
                             os.getenv('SPOTIFY_CLIENT_SECRET', ''),
                             os.getenv('SPOTIFY_AUTH_REDIRECT_URI', ''),
                             token,
                             os.getenv('YOUTUBE_API_KEY', ''))

    def test_sync_from_youtube_music_to_spotify(self):
        id = "RDCLAK5uy_kY7Uomg8uSGAGuvMIKc3HsVg_ipocKTrE"
        user = os.getenv('SPOTIFY_USER', '')

        actual = self.sut.sync_from_youtube_music_to_spotify(id, user)

        assert actual
