from settings import app
from flask import Blueprint, render_template

line_liff_blueprint = Blueprint('line_liff', __name__)


@line_liff_blueprint.route('/line/liff/music', methods=['GET'])
def linechatbot():
    app.logger.info('line bot webhook had been called.')
    liff_id = app.config["LINE_LIFF_ID"]

    return render_template('liff_music.html', liff_id=liff_id)


# @line_liff_blueprint.route('/line/liff/music', methods=['GET'])
# def linechatbot():
#     app.logger.info('line bot webhook had been called.')
#     liff_id = app.config["LINE_LIFF_ID"]
