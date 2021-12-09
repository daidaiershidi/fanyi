# -*- coding: utf-8 -*-
import sys
import uuid
import requests
import hashlib
import time
from imp import reload

import time
import pprint

reload(sys)
class youdao_api():
    # import sys
    # import uuid
    # import requests
    # import hashlib
    # import time
    # from imp import reload
    def __init__(self):
        self.YOUDAO_URL = 'https://openapi.youdao.com/api'
        # self.NECESSARY_KEY = ['q', 'from', 'to', 'appKey', 'salt', 'sign', 'signType', 'curtime']
        self.SUPPLEMENT_KEY = ['ext', 'voice', 'strict', 'vocabld']
        self.APP_KEY = '3190544795136d37'
        self.APP_SECRET = 'VzLYU8JYYWWjnpOokJ2hbGspA9OLS1pl'
        
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.data = {}
        self.set_data()
    def encrypt(self, signStr):
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(signStr.encode('utf-8'))
        return hash_algorithm.hexdigest()   
    def truncate(self, q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]
    def set_data(self):
        self.data['from'] = 'auto'
        self.data['to'] = 'auto'
        self.data['signType'] = 'v3'
        self.data['appKey'] = self.APP_KEY
    def set_api_info(self, APP_KEY, APP_SECRET):
        self.APP_KEY = APP_KEY
        self.APP_SECRET = APP_SECRET
        self.data['appKey'] = self.APP_KEY
    def request(self, q):
        self.data['q'] = q
        
        curtime = str(int(time.time()))
        salt = str(uuid.uuid1())
        signStr = self.APP_KEY + self.truncate(q) + salt + curtime + self.APP_SECRET
        sign = self.encrypt(signStr)
        
        self.data['curtime'] = curtime
        self.signStr = self.APP_KEY + self.truncate(q) + salt + curtime + self.APP_SECRET
        self.data['salt'] = salt
        self.data['sign'] = sign
        return requests.post(self.YOUDAO_URL, data=self.data, headers=self.headers)
    def get_response(self, q):
        response = self.request(q)
        str_response = response.content.decode()
        str_response = str_response.replace('true', 'True')
        str_response = str_response.replace('false', 'False')
        dict_response = eval(str_response)
        if dict_response['errorCode'] != '0':
            return str(dict_response['errorCode'])
        else:
            return [dict_response['translation'][0], dict_response['web'] if 'web' in dict_response.keys() else None]
if __name__ == '__main__':
    youdao_api = youdao_api()
    print(youdao_api.get_response('图卷积真好用'))
            