import logging

from events.default import DefaultEvent
from cache import distribute_cache
from music.music_client_factory import MusicClientFactory
from flask import current_app as app

logger = logging.getLogger('flask.app')

reply_msg_dict = {
    11: "請點選以下網址，透過spotify取得用戶授權\n\n",
    12: "請點選以下網址，透過spotify取得用戶授權\n\n",
    13: "請輸入您喜歡的youtube播放清單連結🥺🥺🥺\n" +
    "輸入格式為 Youtube*{youtube playlist id}",
    14: "請輸入您要新增播放清單的 spotify user name 🥺🥺🥺\n" +
    "輸入格式為 Spotify*{spotify user name}}",
}


class MusicEvent(DefaultEvent):
    """ 音樂事件
    """

    def __init__(self):
        super().__init__()
        self.clientFactory = MusicClientFactory()

    def occurs(self, vocabulary, *args, **kwargs):
        """音樂事件觸發
        """

        if not vocabulary:
            return

        user_id = kwargs.get('user_id', None)
        if not user_id:
            return

        if "同步音樂" in "".join(vocabulary):
            logger.info('同步音樂')
            return self.__music_sync_start_event(user_id)
        elif "Spotify" in "".join(vocabulary):
            logger.info('Spotify')
            return self.__spotify_user_id_event(vocabulary, user_id, "", "")
        elif "Playlist" in "".join(vocabulary):
            logger.info('Youtube Playlist')
            return self.__youtube_playlist_event(vocabulary, user_id, "", "")
        return

    def __music_sync_start_event(self, user_id):

        user_authorized = distribute_cache.get(user_id)
        validate_result = self.__validate_user_authorized(user_authorized)

        if validate_result == 11:
            #  請user 授權spotify
            oauth_client = self.clientFactory.spotify_oauth_client(app.config)
            authorization_url, state = oauth_client.authorize()

            distribute_cache.set(state, {
                "authorization_url": authorization_url,
                "state": state,
                "user_id": user_id
            }, timeout=120)

            reply_message = f"請點選以下網址，透過spotify取得用戶授權\n\n{authorization_url}"

            return reply_message

        if validate_result == 12:
            auth_response_url = user_authorized["auth_response_url"]
            state = user_authorized["state"]
            auth_client = self.clientFactory.spotify_oauth_client(app.config)
            user_authorized["token"] = auth_client.get_token(
                auth_response_url, state)

            distribute_cache.set(user_id, user_authorized, timeout=120)

        validate_result = self.__validate_user_authorized(user_authorized)

        if validate_result == 13:
            return self.__map_reply_message(validate_result)

        if validate_result == 14:
            return self.__map_reply_message(validate_result)

        return self.__music_sync_event(user_authorized["token"],
                                       user_authorized["spotify_user_id"],
                                       user_authorized["youtube_playlist_id"])

    def __youtube_playlist_event(self, vocabulary, user_id):
        user_authorized = distribute_cache.get(user_id)
        validate_result = self.__validate_user_authorized(user_authorized)
        if validate_result > 0 and validate_result <= 13:
            return self.__map_reply_message(validate_result)
        ix = vocabulary.index('*')

        youtube_playlist_id = vocabulary[ix+1:][0]
        user_authorized["youtube_playlist_id"] = youtube_playlist_id
        distribute_cache.set(user_id, user_authorized, timeout=120)

        return self.__music_sync_start_event(user_id)

    def __spotify_user_id_event(self, vocabulary, user_id):
        user_authorized = distribute_cache.get(user_id)
        validate_result = self.__validate_user_authorized(user_authorized)
        if validate_result > 0 and validate_result <= 14:
            return self.__map_reply_message(validate_result)

        ix = vocabulary.index('*')

        spotify_user_id = vocabulary[ix+1:][0]
        user_authorized["spotify_user_id"] = spotify_user_id
        distribute_cache.set(user_id, user_authorized, timeout=120)

        return self.__music_sync_start_event(user_id)

    def __map_reply_message(self, validate_result):
        return reply_msg_dict.get(validate_result, '')

    def __validate_user_authorized(self, user_authorized):
        if not user_authorized \
                or not hasattr(user_authorized, "code") \
                or not hasattr(user_authorized, "auth_response_url"):
            return 11
        elif not hasattr(user_authorized, "token"):
            return 12
        elif not hasattr(user_authorized, "youtube_playlist_id"):
            return 13
        elif not hasattr(user_authorized, "spotify_user_id"):
            return 14

        return 0

    def __music_sync_event(self, token, s_user_id, y_playlist_id):
        client = self.clientFactory.music_sync(app.config, token)

        s_playlist = client.sync_from_youtube_music_to_spotify(
            y_playlist_id, s_user_id)

        title = s_playlist["title"]
        link = s_playlist["link"]

        reply_message = f"恭喜你成功從Youtube Music同步播放清單 [{title}]!! \n" + \
            f"馬上就點開 {link} 到 Spotify 瞧瞧吧 🚀🚀🚀"

        return reply_message
