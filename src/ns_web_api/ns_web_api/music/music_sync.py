import re


class MusicSync:
    def __init__(self,
                 spotify_server_client,
                 spotify_user_client,
                 youtube_music_client) -> None:
        self.spotify_server_client = spotify_server_client
        self.spotify_user_client = spotify_user_client
        self.youtube_music_client = youtube_music_client

    def sync_from_youtube_music_to_spotify(self,
                                           y_playlist_id,
                                           s_user_id):
        """sync music from youtube to spotify
            it will create playlist at spotify

        Args:
            y_playlist_id (string): youtube playlist id
            s_user_id (string): spotify user name
        """
        y_playlist = self.youtube_music_client.playlist(y_playlist_id)

        tracks = []
        for track in y_playlist["tracks"]:
            regex = r"\([\w\s]+\)[\w\s]*"
            test_str = track["title"]
            subst = ""

            keyword = re.sub(regex, subst, test_str, 0, re.MULTILINE)

            track = self.spotify_server_client.query(keyword)

            if track:
                tracks.append(track)

        s_playlist = self.spotify_user_client.create_playlist
        (
            s_user_id,
            y_playlist["name"],
            tracks
        )

        return s_playlist
