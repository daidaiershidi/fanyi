#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import hashlib
import random
import requests


class baidu_api():
    def __init__(self):
        self.apiurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
        self.appid = '20211207001021849'
        self.secretKey = 'iToKRPyf0guXQuMPqzAl'
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.data = {}
        self.set_data()
    def set_api_info(self, appid, secretKey):
        self.appid = appid
        self.secretKey = secretKey
        self.data['appid'] = self.appid
    def set_data(self):
        self.data['from'] = 'auto'
        self.data['to'] = 'auto'
        self.data['appid'] = self.appid
        # salt, sign
    def request(self, q):
        self.data['q'] = q
        
        salt = str(random.randint(32768, 65536))
        sign = self.appid + q + salt + self.secretKey
        sign = hashlib.md5(sign.encode("utf-8")).hexdigest()
        
        self.data['salt'] = salt
        self.data['sign'] = sign
        return requests.post(self.apiurl, data=self.data, headers=self.headers)        
    def get_response(self, q):
        response = self.request(q)
        str_response = response.content.decode()
        dict_response = eval(str_response)
        if 'error_code' in dict_response.keys():
            return str(dict_response['error_code'])
        else:
            return [dict_response['trans_result'][0]['dst']]


if __name__ == '__main__':
    baidu_api = baidu_api()
    res = baidu_api.get_response('百度棒棒')
    print(res)
 
