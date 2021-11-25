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

    if not state_info:
        distribute_cache.set(state_info["user_id"], {
            "code": code,
            "state": state,
            "auth_response_url": re.sub(r'http:\/\/',  request.url, "https://")
        }, timeout=120)

        app.logger.info('set spotify authorized code in cache: ok.')

        bot_service = LYCLineBot(app.config['LINEBOT_CHANNEL_ACCESS_TOKEN'],
                                 app.config['LINEBOT_CHANNEL_SECRET'])

        push_msg = "Spotify 授權完成！ 請輸入您要新增播放清單的 spotify user name 🥺🥺🥺\n" + \
            "輸入格式為 Spotify*{spotify user name}"

        bot_service.send_message(push_msg, state_info["user_id"])

    return request.url
