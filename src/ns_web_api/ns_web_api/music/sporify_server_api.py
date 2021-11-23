import requests
from requests.auth import HTTPBasicAuth
from jsonpath import jsonpath


class SpotifyServerApi:

    def __init__(self, client_id, client_secret) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.domain_url = "https://api.spotify.com"
        self.auth_domain = "https://accounts.spotify.com"
        self.auth_client_redentials()
        self.session = self.__create_request()

    def auth_client_redentials(self):
        payload = {"grant_type": "client_credentials"}
        url = f"{self.auth_domain}/api/token"
        headers = {"content-type": "application/x-www-form-urlencoded",
                   "user-agent": "lyc-music-app/0.0.1"}
        auth = HTTPBasicAuth(self.client_id, self.client_secret)
        resp = requests.post(url,
                             data=payload,
                             verify=True,
                             auth=auth,
                             headers=headers)

        if resp.status_code == requests.codes.ok:
            self._access_token = resp.json()
            return self.client_credentials_token

        return ""

    def query(self, q):
        url = f"{self.domain_url}/v1/search"

        params = {
            "q": q,
            "type": "track",
            "market": "TW",
            "offset": 0,
            "limit": 1
        }
        resp = self.session.get(url, params=params)

        if resp.status_code == requests.codes.ok:
            response = resp.json()
            tracks = jsonpath(response, "$.tracks.items")[0]
            if len(tracks) > 0:

                track = tracks[0]

                return {
                    "id": track["id"],
                    "name": track["name"],
                    "artist": track["artists"][0]["name"],
                    "uri": track["uri"],
                }

        return None

    @property
    def client_credentials_token(self):
        return self._access_token["access_token"] \
            if hasattr(self, "_access_token") \
            else ""

    def __create_request(self):
        session = requests.Session()
        headers = {'user-agent': 'lyc-music-app/0.0.1',
                   'Authorization': f'Bearer {self.client_credentials_token}'}
        session.headers.update(headers)
        return session
