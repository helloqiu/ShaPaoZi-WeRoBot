# -*- coding: utf-8 -*-

from werobot import WeRoBot
from werobot.utils import to_text
import requests
import time

token = ''
encoding_aes_key = ''
app_id = ''

robot = WeRoBot(token=token,
                encoding_aes_key=encoding_aes_key,
                app_id=app_id)


@robot.text
def search(message):
    if to_text(message.content) == to_text('status'):
        url = 'http://127.0.0.1:8000/api/status'
        result = requests.get(url).json()
        return result['total']
    url = 'http://127.0.0.1:8000/api/search/%s' % message.content
    result = requests.get(url).json()
    return_value = ''
    return_value += '搜索到 %d 个结果:\n' % result['total']
    max_page = result['max_page']
    result = requests.get('%s/page/1' % url).json()
    for r in result['results']:
        return_value += '=' * 5
        return_value += '\n'

        r['last_seen'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(r['last_seen']))
        r['length'] = '%dMB' % int(r['length'] / 1024 / 1024)

        return_value += '名称: %s\n' % r['title']
        return_value += '大小: %s\n' % r['length']
        return_value += '记录时间: %s\n' % r['last_seen']
        return_value += '详情页: http://www.shapaozi.me/detail/%s\n' % r['infohash']
        return_value += '=' * 5
        return_value += '\n'

    if max_page > 1:
        return_value += '更多结果请点击: http://www.shapaozi.me/search/%s' % message.content

    return return_value


@robot.subscribe
def hello():
    return '欢迎关注超级可爱的 ShaPaoZi ( ˙˘˙ )\n请直接回复查询内容。'


robot.run(host='localhost', port=5000, server='gunicorn')
