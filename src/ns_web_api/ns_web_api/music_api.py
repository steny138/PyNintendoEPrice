from settings import app
from flask import Blueprint, request
from cache import distribute_cache
from bot.line import LYCLineBot
import re

music_api_blueprint = Blueprint('music_api', __name__)


@music_api_blueprint.route("/api/v1/music/spotify/oauth2/callback", methods=['GET', 'POST'])
def oauth2_callback():
    app.logger.info('music api had been called.')

    code = request.values.get("code")
    state = request.values.get("state")
    state_info = distribute_cache.get(state)
    if state_info:
        user_id = state_info.get("user_id", '')
        app.logger.info(f"found user id: {user_id}")
        url = request.url.replace("http://", "https://")
        distribute_cache.set(user_id, {
            "code": code,
            "state": state,
            "auth_response_url": url
        }, timeout=120)

        user_authorized = distribute_cache.get(user_id)

        app.logger.info(user_authorized)
        app.logger.info('set spotify authorized code in cache: ok.')

        bot_service = LYCLineBot(app.config['LINEBOT_CHANNEL_ACCESS_TOKEN'],
                                 app.config['LINEBOT_CHANNEL_SECRET'])

        push_msg = "Spotify 授權完成！ 請輸入您喜歡的youtube播放清單連結🥺🥺🥺\n" + \
            "輸入格式為 Playlist*{youtube playlist id}"

    bot_service.send_message(push_msg, state_info["user_id"])

    return request.url
