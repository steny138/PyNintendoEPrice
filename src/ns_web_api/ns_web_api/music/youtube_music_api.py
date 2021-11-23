
import requests


class YoutubeMusicApi:

    def __init__(self, api_key) -> None:
        self.key = api_key
        self.domain_url = "https://www.googleapis.com"
        self.session = self.__create_request()

    def playlist(self, id):
        url = f"{self.domain_url}/youtube/v3/playlists"

        resp = self.session.get(url, params={
            "id": id,
            "part": "contentDetails,player,snippet,status"
        })

        tracks = {}
        response = resp.json()
        playlist = response["items"][0]
        if resp.status_code == requests.codes.ok:
            for track in self.playlist_tracks(id):
                if track["id"] not in tracks:
                    tracks[track["id"]] = track

        return {
            "playlist_id": id,
            "name": playlist["snippet"]["title"],
            "description": playlist["snippet"]["description"],
            "tracks": [tracks[key] for key in tracks],
            "tracks_info": {
                "tracks_count": playlist["contentDetails"]["itemCount"]
            },
        }

    def playlist_tracks(self, playlist_id, page="", size=50, preToken=""):
        url = f"{self.domain_url}/youtube/v3/playlistItems"

        session = self.__create_request()
        resp = session.get(url, params={
            "playlistId": playlist_id,
            "part": "id,contentDetails,snippet,status",
            "maxResults": size,
            "pageToken": page
        })

        if resp.status_code == requests.codes.ok:
            response = resp.json()
            items = response["items"]

            for item in items:
                track = {
                    "id": item["id"],
                    "title": item["snippet"]["title"],
                    "vid": item["contentDetails"]["videoId"],
                }

                yield track

            goNext = "nextPageToken" in response

            if "prevPageToken" in response and preToken != "":
                goNext &= (response["prevPageToken"] != preToken)

            if goNext:
                yield from self.playlist_tracks(
                    playlist_id,
                    page=response["nextPageToken"],
                    preToken=response.get("prevPageToken", ""))

    def __create_request(self):
        session = requests.Session()
        headers = {'user-agent': 'lyc-music-app/0.0.1'}
        session.headers.update(headers)
        session.params["key"] = self.key
        return session
