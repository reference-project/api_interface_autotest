#!/usr/bin/env python
# encoding=utf8
import hashlib
import hmac
import json

import requests
import time as t

'''
这个是最基础的版本，来自研发的使用文档
'''
app_id = 'com.example.demo' # 应用标识
app_key = 'f394e5f5887b4dc483fb69a54f561d8f' # 秘钥

user_id = '100046' # 登录用户标识
user_name = 'dangtao' # 登录用户账号
op_type = 'LOGIN' # 操作类型
op_id = '1d01cc313cc6449e9d6f57a447698dc4' # 操作标识
scene = '2001' # 场景标识
device_info = '集成SDK获取' # 设备信息
time = str(int(t.time())) # 时间戳

#接口相关参数
params = {
    'app_id': app_id,
    'user_id': user_id,
    'user_name': user_name,
    'op_type': op_type,
    'op_id': op_id,
    'scene': scene,
    'time': time,
    'device_info': device_info
}

param_values = ''
for k in sorted(params.keys()) :
    param_values = '%s%s' % (param_values, params[k])

#生成签名
signature = hmac.new(app_key, param_values, hashlib.sha256).hexdigest()
params['signature'] = signature

#发送请求
url = ' http://ifds1.trusfort.com/api/risk'
r = requests.post(url, data = json.dumps(params))
print r.json()
