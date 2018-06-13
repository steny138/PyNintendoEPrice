from main import app
from bot.line import LYCLineBot
from flask import Blueprint, jsonify, request
import json
line_bot_api_blueprint = Blueprint('line_bot_api', __name__)

@line_bot_api_blueprint.route('/api/v1/chatbot/line/webhook', methods=['POST'])
def linechatbot():
    app.logger.info('line bot webhook had been called.')

    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    app.logger.info('signature: %s', signature)

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info('body: %s', body)

    bot_service = LYCLineBot(app.config['LINEBOT_CHANNEL_ACCESS_TOKEN'],app.config['LINEBOT_CHANNEL_SECRET'])
    bot_service.reply_message('', body, signature)

    return 'OK'

@line_bot_api_blueprint.route('/api/v1/chatbot/line/message/<msg>')
def linechatbot_send_message(msg):
    bot_service = LYCLineBot(app.config['LINEBOT_CHANNEL_ACCESS_TOKEN'],app.config['LINEBOT_CHANNEL_SECRET'])
    bot_service.send_message(msg)
    return jsonify({'message': msg})

@line_bot_api_blueprint.route('/api/v1/chatbot/facebook/webhook')
def facebook_chatbot():
    pass


