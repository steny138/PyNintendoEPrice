from settings import app
from flask import Blueprint, jsonify, request
from cache import distribute_cache

music_api_blueprint = Blueprint('music_api', __name__)


@music_api_blueprint.route('/api/v1/music/login', methods=['POST'])
def linechatbot():
    app.logger.info('music api had been called.')

    user = distribute_cache.get(user_id)

    if not user:


@music_api_blueprint.route("/api/v1/music/spotify/oauth2/callback", methods=['POST'])
def oauth2_callback():
    print(request.values)

    return request.url
