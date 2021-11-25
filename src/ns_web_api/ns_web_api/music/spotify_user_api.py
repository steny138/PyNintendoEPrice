import logging
import requests
from requests_oauthlib import OAuth2Session

logger = logging.getLogger('flask.main')


class SpotifyUserApi:

    def __init__(self, client_id, client_secret, token_dict, redirect_uri) -> None:
        self.auth_domain = "https://accounts.spotify.com"
        self.domain = "https://api.spotify.com"
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token_dict
        self.redirect_uri = redirect_uri
        self.session = self.__create_session()

    def create_playlist(self, user_id, title, tracks):

        playlist = self._create_playlist(user_id, title)

        if not playlist:
            print("\nno playlist")
            return None

        append_result = self._append_tracks_in_playlist(playlist["id"], tracks)

        if not append_result:
            logger.warning("!!! append_tracks_in_playlist failed !!!")
        return playlist

    def _create_playlist(self, user_id, title):
        url = f"{self.domain}/v1/users/{user_id}/playlists"
        data = {
            "name": title,
            "public": True,
            "collaborative": False,
            "description": "Automation PLAYLIST FROM LYC corp."
        }
        resp = self.session.post(url,
                                 json=data,
                                 headers={"Content-Type": "application/json"})

        if resp.status_code == requests.status_codes.codes.created:
            response = resp.json()
            return {
                "id": response["id"],
                "uri": response["uri"],
                "title": response["name"],
                "link": response["external_urls"]["spotify"]
            }
        logger.warning(resp.text)

    def _append_tracks_in_playlist(self, playlist_id, tracks):
        url = f"{self.domain}/v1/playlists/{playlist_id}/tracks"
        data = {
            "uris": [track["uri"] for track in tracks],
            "position": 0,
        }

        resp = self.session.post(url, json=data)

        return resp.status_code == requests.status_codes.codes.created

    def current_user(self, user_id):
        url = f"{self.domain}/v1/users/{user_id}"

        resp = self.session.get(url)

        if resp.status_code == requests.status_codes.codes.ok:
            return resp.text

    def __create_session(self):

        # Note that these are Google specific scopes
        scope = ['playlist-modify-public']

        refresh_url = f"{self.auth_domain}/api/token"

        extra = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        def token_updater(token):
            self.token = token
        oauth = OAuth2Session(self.client_id,
                              token=self.token,
                              redirect_uri=self.redirect_uri,
                              auto_refresh_url=refresh_url,
                              auto_refresh_kwargs=extra,
                              scope=scope,
                              token_updater=token_updater)

        return oauth
