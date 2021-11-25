import logging

from events.default import DefaultEvent
from cache import distribute_cache
from music.music_client_factory import MusicClientFactory
from flask import current_app as app

logger = logging.getLogger('flask.app')


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

        if "同步音樂" in vocabulary:
            logger.info('同步音樂')
            return self.__music_event(vocabulary)
        elif "台鐵" in vocabulary:
            logger.info("traffic-台鐵")
        elif "統聯" in vocabulary:
            logger.info("traffic-統聯")
        elif "國光" in vocabulary:
            logger.info("traffic-國光")

        return

    def __music_sync_event(self,
                           vocabulary,
                           user_id,
                           y_playlist_id,
                           s_user_id):

        user = distribute_cache.get(user_id)

        if not user:
            #  請user 授權spotify
            oauth_client = self.clientFactory.spotify_oauth_client(app.config)
            authorization_url, state = oauth_client.authorize()

            distribute_cache.set(user_id, {
                "authorization_url": authorization_url,
                "state": state
            })

            reply_message = f"請點選以下網址，透過spotify取得用戶授權\n\n{authorization_url}"

            return reply_message

        token = user["token"]
        client = self.clientFactory.music_sync(app.config, token)

        s_playlist = client.sync_from_youtube_music_to_spotify(
            y_playlist_id, s_user_id)

        title = s_playlist["title"]
        link = s_playlist["link"]

        reply_message = f"恭喜你成功從Youtube Music同步播放清單 [{title}]!! \n" + \
            f"馬上就點開 {link} 到 Spotify 瞧瞧吧 🚀🚀🚀"

        return reply_message
