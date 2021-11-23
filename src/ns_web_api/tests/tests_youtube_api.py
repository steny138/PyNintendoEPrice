
from ns_web_api.music.youtube_music_api import YoutubeMusicApi
from dotenv import load_dotenv
import os


class TestYoutubeApi:

    def setup_class(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(dotenv_path, override=True)
        self.sut = YoutubeMusicApi(os.getenv('YOUTUBE_API_KEY', ''))

    def test_youtube_palylist(self):
        id = "RDCLAK5uy_kY7Uomg8uSGAGuvMIKc3HsVg_ipocKTrE"

        actual = self.sut.playlist(id)

        assert actual
        assert len(actual["tracks"]) > 1
        assert actual["tracks_info"]["tracks_count"] > 1

    def test_youtube_tracks(self):
        id = "RDCLAK5uy_kY7Uomg8uSGAGuvMIKc3HsVg_ipocKTrE"

        actual = self.sut.playlist_tracks(id)

        assert len(list(actual)) > 1
