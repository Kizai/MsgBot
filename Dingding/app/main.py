# -*- coding: UTF-8 -*-
"""
-------------------------------------------------
   FileName：        main   
   Description：     钉钉消息通知机器人API服务
   Author：          kizai
   Date：            2023/3/1
-------------------------------------------------
"""
import os.path
from flask import request, Flask, jsonify
from flask_json import as_json, FlaskJSON
import requests
import time
import hmac
import urllib
import base64
import hashlib
import json
import logging

log_path = './run.log'
logging.basicConfig(filename=log_path, filemode='a+', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(filename)s %(funcName)s %(lineno)d %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")

config_path = os.path.join(os.path.dirname(__file__), "config.json")

# 读取配置文件
with open(config_path, 'r', encoding='utf8') as f:
    config = json.load(f)

webhook = config['ws']['webhook']
secrets = config['ws']['secret']

app = Flask(__name__)
FlaskJSON(app)


# 加签
def signature_url(webhook_url: str, secret: str):
    # 生成当前时间戳，单位是毫秒，与请求调用时间误差不能超过1小时
    timestamp = str(round(time.time() * 1000))
    # 修改编码格式为utf-8
    secret_enc = secret.encode('utf-8')
    # 将timestamp和secret合并
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    # 修改编码格式为utf-8
    string_to_sign_enc = string_to_sign.encode('utf-8')
    # 将字段进行加密，加密类型采用sha256
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    # 生成请求的URL，WebHook地址
    post_url = ("%s&timestamp=%s&sign=%s" % (webhook_url, timestamp, sign))
    logging.info(post_url)
    return post_url


# 发送Text信息
def send_msg(text: str, is_at_all: str, at_user_id: str = None):
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    url = signature_url(webhook, secrets)
    data = {
        "msgtype": "text",
        "text": {
            "content": text
        },
        "at": {
            "atMobiles": [
            ],
            "atUserIds": [at_user_id
                          ],
            "isAtAll": is_at_all
        }
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    logging.info(r.text)
    return r.text


# 发送MarkDown信息
def send_markdown_msg(text: str, is_at_all: str = False, at_user_id: str = None):
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    url = signature_url(webhook, secrets)
    data = {
        "msgtype": "markdown",
        "markdown": {"title": 'Markdown Message',
                     "text": text},
        "at": {
            "atMobiles": [
            ],
            "atUserIds": [at_user_id
                          ],
            "isAtAll": is_at_all
        }
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    logging.info(r.text)
    return r.text


# 检查服务端口是否正常
@app.route('/api/v1', methods=['GET', 'POST'])
def check():
    return jsonify({"code": 0, "message": config['msg']['0']})


# 发送文本信息接口
@app.route('/api/v1/text', methods=['POST'])
@as_json
def dingbot_text():
    if request.method == 'POST':
        try:
            data = request.args
            message = data['message']
            is_at_all = data.get('is_at_all')
            at_user_id = data.get('at_user_id')
            if message:
                send_msg(message, is_at_all, at_user_id)
                return jsonify({"code": 0, "message": config['msg']['0']})
            else:
                logging.error(config['msg']['-1'])
                return jsonify({"code": -1, "message": config['msg']['-1']})
        except:
            logging.error(config['msg']['400'])
            return jsonify({"code": 400, "message": config['msg']['400']})


# 发送markdown信息接口
@app.route('/api/v1/md', methods=['POST'])
@as_json
def dingbot_link():
    if request.method == 'POST':
        try:
            data = request.args
            text = data['text']
            message_url = data['message_url']
            is_at_all = data.get('is_at_all')
            at_user_id = data.get('at_user_id')
            if text and message_url:
                if at_user_id:
                    text_content = "{},[消息链接]({}),\n@{}".format(text, message_url, at_user_id)
                    send_markdown_msg(text_content, is_at_all, at_user_id)
                    return jsonify({"code": 0, "message": config['msg']['0']})
                else:
                    text_content = "{},[消息链接]({})".format(text, message_url)
                    send_markdown_msg(text_content, is_at_all)
                    return jsonify({"code": 0, "message": config['msg']['0']})
            else:
                logging.error(config['msg']['-1'])
                return jsonify({"code": -1, "message": config['msg']['-1']})
        except:
            logging.error(config['msg']['400'])
            return jsonify({"code": 400, "message": config['msg']['400']})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config['port'], debug=True)
