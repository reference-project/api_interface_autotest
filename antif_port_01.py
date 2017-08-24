#!/usr/bin/env python
# encoding=utf8
import hashlib
import hmac
import json
import random
import threading
from datetime import datetime
from xml.dom import minidom

import requests

import time
import time as t
from time import ctime

'''
性能测试版本1
可配置运行时间，并发数
可配置场景、测试地址、pkgname
appid 改变 appkey也要改变
'''

#========================================Start of parameter configuration========================================
# 性能测试参数设置
ext = 2  # 运行时间，单位分钟
vu = 10  # 并发数，VU

#应用配置
#自定义应用
# appid = 'com.huang.shuai'
# appkey = 'VzqSPL0oll8IoG/4CkC/mN8AE6DlMr/nqf/5fixolMFQLpTNW3GSGT2pZNtHcaF7'
# ver = '02'
# sen = 'HSDL'    #测试场景-登录

#标准应用
appid = 'com.example.demo'
appkey = 'f394e5f5887b4dc483fb69a54f561d8f'
ver = '01'
sen = 'HSDL_1'    #测试场景-登录

#标准应用-场景参数配置
# sen = 'HT10001'  # 场景标识-登录
# sen = 'HT20001'  # 场景标识-注册
# sen = 'HT70001'  # 场景标识-兑换礼品
# sen = 'HT90001'  # 场景标识-每日转盘
# sen = 'HT100001'  # 场景标识-创建群组

#测试地址配置
url_risk = 'http://192.168.1.113/api/risk'  # 测试地址-风控
url_report = 'http://192.168.1.113/api/logreport/businesslog'  # 测试地址-上报事件
# url_risk = 'http://ifds1.trusfort.com/api/risk'#阿里云地址-风控
# url_report = 'http://ifds1.trusfort.com/api/logreport/businesslog'#阿里云地址-上报事件

#测试设备
# dev = 'Xiaomi_MI5'
# dev = 'HUAWEI_NXT_AL10'
dev = 'Nexus_5'
# dev = 'Coolpad_T1'
# dev = 'HONOR_DUK_AL20'
# dev = 'Redmi_Note_4'

#========================================Ecd of parameter configuration========================================


# 读取xml文件
def readxml(node):
    dom = minidom.parse('Devices_Info.xml')
    value = dom.getElementsByTagName(node)[0].childNodes[0].nodeValue
    return value


time = str(int(time.time()))# 时间戳


def login():
    print "starting time is %s" % ctime()
    # 定义用户手机号，生成100个号码，13263290100~13263290199
    phone = []
    for q in range(100000, 999999):
        phone.append("18600" + str(q))
        q += 1
    st = datetime.now().minute
    cnt = 1
    var = 1
    while var == 1:
        # total = 36000
        # for cnt in range(1, total):
        # do somethong
        # 循环所有手机号
        for index in range(len(phone)):
            cnt += 1
            # print phone
            app_id = appid  # 应用标识
            app_key = appkey  # 秘钥
            user_id = phone[index]  # 登录用户标识
            user_name = phone[index]  # 登录用户账号
            op_type = 'LOGIN'  # 操作类型
            tmp_op_id = str(random.randint(100000000, 999999999))
            # print '----------------------'+tmp_op_id
            op_id = '1d01cc313cc6449e9d6fdc4' + tmp_op_id  # 操作标识
            scene = sen # 场景标识
            device_info = readxml(dev)  # 设备信息
            # print device_info
            # print device_info
            version = ver

            # 接口相关参数
            params = {
                'app_id': app_id,
                'user_id': user_id,
                'user_name': user_name,
                'op_type': op_type,
                'op_id': op_id,
                'scene': scene,
                'time': time,
                'device_info': device_info,
                'version': version
            }

            param_values = ''
            for k in sorted(params.keys()):
                param_values = '%s%s' % (param_values, params[k])

            # 生成签名
            signature = hmac.new(app_key, param_values, hashlib.sha256).hexdigest()
            params['signature'] = signature

            # 风控事件
            url = url_risk
            r = requests.post(url, data=json.dumps(params))

            t.sleep(1)

            # 上报事件
            url1 = url_report
            r1 = requests.post(url1, data=json.dumps(params))

            et = datetime.now().minute
            tt = (et - st) + 1
            if (tt > ext):  # >后面加分钟数
                break
            else:
                continue
            break

        break

    print 'cnt is %s' % cnt
    print "ending time is %s" % ctime()


# 配置线程数量
def work():
    t = []
    for i in range(vu):
        t.append(threading.Thread(target=login))
    for j in t:
        j.start()


# 开启线程
if __name__ == '__main__':
    # for t in threads:
    #     t.setDaemon(True)
    #     t.start()
    work()
