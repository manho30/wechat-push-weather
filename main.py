'''
!/usr/bin/env python
-*- coding: utf-8 -*-

__author__ = "manho"
__copyright__ = "©2022 manho All Right Reserved"

'''

import datetime
import logging

import requests


# enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# config
weather_key = ''
current_state = ''
templete_id = ''
app_id = ''
app_secret = ''
url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(app_id, app_secret) 

def get_access_token():
    return requests.get(url).json().get('access_token')


love_start = datetime.datetime.strptime('yyyy-mm-dd', '%Y-%m-%d') # 在一起的时候 格式不可错！
now = datetime.datetime.now()

# already love days
love_days = (now - love_start).days

# birthday
birthday = datetime.datetime.strptime('{}-mm-dd'.format(now.year), '%Y-%m-%d') # 对方生日的时候 格式不可错！
days_to_birthday = (birthday - now).days

# LEFT SOME TEXT U WANT TO DISPLAY
one_sentence = ''

# ur girls openid
touser = ''

def wheater():
    return requests.get('https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&lang=zh_cn&units=metric'.format(current_state, weather_key)).json()
    
def love_story():
    return requests.get('https://api.vvhan.com/api/love').text
    
data = {
    'touser': touser,
    'template_id': templete_id,
    'data': {
        'ur_sentence': {
            'value': one_sentence,
            'color': '#000'
        },
        'love_days': {
            'value': '我们已经恋爱了{}天啦 '.format(love_days),
            'color': '#000'
        },
        'days_to_birthday': {
            'value': '再多{}天就是你的生日啦!!!'.format(days_to_birthday) if days_to_birthday > 0 else '今天是宝宝的生日呀!!!',
            'color': '#000'
        },
        'weather': {
            'value': '今天天气：{}\n今天温度： {}度'.format(wheater().get('weather')[0].get('description'), ('%.1f'%wheater().get('main').get('temp'))),
            'color': '#000'
        },
        'love_story': {
            'value': love_story(),
            'color': '#FF0000'
        }
    }
    
}

def send_template_message():
    res = requests.post('https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(get_access_token()), json=data).json()
    if res.get('errcode') == 0:
        logger.info('send template message success')
        return res
    else:
        logger.error('send template message failed')
        logger.error(res)
        return res
        
if __name__ == '__main__':
    send_template_message()
