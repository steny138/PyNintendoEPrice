import requests
from requests.auth import HTTPBasicAuth
from jsonpath import jsonpath


class SpotifyApi:

    def __init__(self, client_id, client_secret) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.domain_url = "https://api.spotify.com"

        self.auth_client_redentials()
        self.session = self.__create_request()

    def auth_client_redentials(self):
        payload = {"grant_type": "client_credentials"}
        url = "https://accounts.spotify.com/api/token"
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
            track = jsonpath(response, "$.tracks.items.0")[0]
            return {
                "id": track["id"],
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "uri": track["uri"],
            }

        return None

    @property
    def client_credentials_token(self):
        return self._access_token["access_token"]

    def __create_request(self):
        session = requests.Session()
        headers = {'user-agent': 'lyc-music-app/0.0.1',
                   'Authorization': f'Bearer {self.client_credentials_token}'}
        session.headers.update(headers)
        return session


if __name__ == '__main__':
    api = SpotifyApi("40375dc7a37b496d84ae5468bc484e9f",
                     "5eda3296dd804b93a2a78603902f09ce")
    api.auth_client_redentials()
