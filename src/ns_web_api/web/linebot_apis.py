from main import app
from bot.line import LYCLineBot
from mask_sale import timetable
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


@line_bot_api_blueprint.route('/api/v1/chatbot/line/boardcast/<msg>')
def linechatbot_boardcast(msg):
    bot_service = LYCLineBot(app.config['LINEBOT_CHANNEL_ACCESS_TOKEN'],app.config['LINEBOT_CHANNEL_SECRET'])
    bot_service.boardcast(msg)
    return jsonify({'message': msg})


@line_bot_api_blueprint.route('/api/v1/chatbot/line/mask/boardcast')
def linechatbot_mask_boardcast():
    """口罩購買提醒廣播
    """
    bot_service = LYCLineBot(app.config['LINEBOT_CHANNEL_ACCESS_TOKEN'],app.config['LINEBOT_CHANNEL_SECRET'])

    schedule_msg = timetable.build_alert_msg()
    
    if schedule_msg:
        bot_service.boardcast(schedule_msg)

    return jsonify({'message': schedule_msg})


@line_bot_api_blueprint.route('/api/v1/chatbot/facebook/webhook')
def facebook_chatbot():
    pass