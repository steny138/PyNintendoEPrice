from settings import app
from flask import Blueprint, request, redirect
from cache import distribute_cache
from bot.line import LYCLineBot
from requests import status_codes
from urllib.parse import urlparse, parse_qs
from music.music_client_factory import MusicClientFactory

music_api_blueprint = Blueprint('music_api', __name__)


@music_api_blueprint.route("/music/spotify/oauth2/callback",
                           methods=['GET', 'POST'])
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

    liff_id = app.config["LINE_LIFF_ID"]

    return redirect(f"https://liff.line.me/{liff_id}")  # request.url


@music_api_blueprint.route("/api/v1/music/spotify/playlist",
                           methods=['POST'])
def create_playlist():
    app.logger.info('music api had been called.')

    data = request.get_json()
    user_id = data["line_id"]

    user_authorized = distribute_cache.get(user_id)

    clientFactory = MusicClientFactory()

    if not user_authorized:
        oauth_client = clientFactory.spotify_oauth_client(app.config)
        authorization_url, state = oauth_client.authorize()

        distribute_cache.set(state, {
            "authorization_url": authorization_url,
            "state": state,
            "user_id": user_id
        }, timeout=120)

        return {
            "error_msg":  "get authorization from spotify first",
            "authorization_url": authorization_url,
            "state": state
        }, status_codes.codes.unauthorized

    if not data.get("youtube_playlist_link", '') or \
            not data.get("spotify_user_id", ''):
        return {
            "error_msg":  "cannot sync without playlist link",
        }, status_codes.codes.bad_request

    query = parse_qs(urlparse(data["youtube_playlist_link"]).query)
    y_playlist_id = query.get("list", "")

    if not y_playlist_id:
        return {
            "error_msg":  "invalid playlist link",
        }, status_codes.codes.bad_request

    if "token" not in user_authorized:

        auth_client = clientFactory.spotify_oauth_client(app.config)

        user_authorized["token"] = auth_client.get_token(
            user_authorized["auth_response_url"],
            user_authorized["state"])

        distribute_cache.set(user_id, user_authorized, timeout=120)

    sync_client = clientFactory.music_sync(
        app.config,
        user_authorized["token"])

    playlist = sync_client.sync_from_youtube_music_to_spotify(
        y_playlist_id,
        data['spotify_user_id'])

    return playlist
