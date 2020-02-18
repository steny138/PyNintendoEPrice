import json
import pandas as pd
from flask import Blueprint, jsonify, request, abort

mask_api_blueprint = Blueprint('mask_api', __name__)

@mask_api_blueprint.route('/api/v1/mask/pharmacy', methods=['GET'])
def find_pharmacy_reserve():
    ids = request.args.get('ids')
    if not ids:
        abort(404)

    ids = ids.split(',')

    df = pd.read_csv("https://data.nhi.gov.tw/Datasets/Download.ashx?rid=A21030000I-D50001-001&l=https://data.nhi.gov.tw/resource/mask/maskdata.csv")

    # filter pharmacy identity
    df = df[df['醫事機構代碼'].isin(ids)]
    df = df.rename(columns={
        "醫事機構代碼": "id", 
        "醫事機構名稱": "name", 
        "醫事機構地址":"address",
        "醫事機構電話":"phone",
        "成人口罩剩餘數":"adult",
        "兒童口罩剩餘數":"child",
        "來源資料時間": "update_time"})
    
    mask_dict = df.to_dict(orient='records')

    return jsonify({'data': mask_dict})