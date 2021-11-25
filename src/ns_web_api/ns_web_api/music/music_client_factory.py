from .music_sync import MusicSync
from .spotify_oauth import SpotifyOAuth2
from .sporify_server_api import SpotifyServerApi
from .spotify_user_api import SpotifyUserApi
from .youtube_music_api import YoutubeMusicApi


class MusicClientFactory:
    def music_sync(self, config: dict, token):
        return MusicSync(self.spotify_server_client(config),
                         self.spotify_user_client(config, token),
                         self.youtube_client(config))

    def spotify_server_client(self, config: dict):
        return SpotifyServerApi(config["SPOTIFY_CLIENT_ID"],
                                config["SPOTIFY_CLIENT_SECRET"])

    def spotify_oauth_client(self, config: dict):
        return SpotifyOAuth2(config["SPOTIFY_CLIENT_ID"],
                             config["SPOTIFY_CLIENT_SECRET"],
                             config["SPOTIFY_AUTH_REDIRECT_URI"])

    def spotify_user_client(self, config: dict, token):
        return SpotifyUserApi(config["SPOTIFY_CLIENT_ID"],
                              config["SPOTIFY_CLIENT_SECRET"],
                              token,
                              config["SPOTIFY_AUTH_REDIRECT_URI"])

    def youtube_client(self, config: dict):
        return YoutubeMusicApi(config["YOUTUBE_API_KEY"])
