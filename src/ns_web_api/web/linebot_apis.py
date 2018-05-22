from main import app
from bot.line import LYCLineBot
from flask import Blueprint, jsonify, request

line_bot_api_blueprint = Blueprint('line_bot_api', __name__)

@line_bot_api_blueprint.route('/api/v1/chatbot/line/webhook', methods=['POST'])
def linechatbot():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)

    return jsonify({'signature':signature, 'body': body})

@line_bot_api_blueprint.route('/api/v1/chatbot/line/message/<msg>')
def linechatbot_send_message(msg):
    bot_service = LYCLineBot()
    bot_service.send_message(msg)
    return jsonify({'message': msg})

@line_bot_api_blueprint.route('/api/v1/chatbot/facebook/webhook')
def facebook_chatbot():
    pass


