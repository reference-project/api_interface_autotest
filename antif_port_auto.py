#!/usr/bin/env python
# encoding=utf8
import hashlib
import hmac
import json
import random
import urllib2
from datetime import datetime
from xml.dom import minidom
import time as t

import time
from time import ctime

'''
自动化测试脚本
'''

# 时间参数
time = str(int(t.time()))  # 时间戳


# 读取xml文件
def readxml(node):
    dom = minidom.parse('devices_Info.xml')
    value = dom.getElementsByTagName(node)[0].childNodes[0].nodeValue
    return value


def risk_report_all_sen():
    print "START TIME IS: %s" % ctime()
    # 固定参数
    cnt = 0
    var = 1
    # 可变参数
    name_no = 0
    scene_no = 0
    dev_no = 0
    # 定义循环次数
    for k in range(0, var):

        name_no = random.randint(0, 100)
        dev_no = random.randint(0, 5)
        scene_no = random.randint(0, 5)

        cnt += 1
        # 测试地址配置
        # url_risk = 'http://192.168.1.112:6080/api/risk'
        # url_report = 'http://192.168.1.112:6080/api/logreport/businesslog'
        # print url_risk
        # print url_report
        # 阿里云地址配置
        url_risk = 'http://ifds1.trusfort.com:8080/api/risk'
        url_report = 'http://ifds1.trusfort.com:8080/api/logreport/businesslog'

        # 生成app_id，这个参数一般是固定的，如果APPID改变appkey也改变
        app_id = 'com.example.demo'
        app_key = 'f394e5f5887b4dc483fb69a54f561d8f'

        # 测试使用的app_id app_key
        # app_id = 'com.huang.shuai'
        # app_key = 'VzqSPL0oll8IoG/4CkC/mN8AE6DlMr/nqf/5fixolMFQLpTNW3GSGT2pZNtHcaF7'

        # 生成手机号码，用于user_id  user_name
        phone = []
        for q in range(1000, 9999):
            phone.append("1860000" + str(q))
            q += 1

        user_id = phone[name_no]
        user_name = phone[name_no]

        # 参数化场景场景与表示一致
        op_type_tmp = ['LOGIN', 'REGISTER', 'CASH_GIFT', 'WIN_AWARD', 'DAILY_TURNTABLE', 'CREATE_GROUP']
        op_type = op_type_tmp[scene_no]
        scene_tmp = ['HT10001', 'HT20001', 'HT70001', 'HT80001', 'HT90001', 'HT100001']
        scene = scene_tmp[scene_no]

        # 操作标识
        tmp_op_id = str(random.randint(1000, 9999))
        op_id = '1d01cc313cc6449e9d6fdce5g84' + tmp_op_id

        # 设备指纹
        tmp_device_info = ['Xiaomi_MI5', 'HUAWEI_NXT_AL10', 'Nexus_5', 'Coolpad_T1', 'HONOR_DUK_AL20', 'Redmi_Note_4']
        dev = tmp_device_info[dev_no]
        device_info = readxml(dev)

        # 版本，默认为01
        version = '01'
        # version = '02'

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

        print "app_id: " + app_id
        print "device_info: " + dev
        print"user_id: " + user_id
        print"scene: " + scene
        print"op_type: " + op_type
        print"time: " + time
        print"user_name: " + user_name
        print "app_key: " + app_key
        print"op_id: " + op_id
        print"version: " + version

        param_values = ''
        for k in sorted(params.keys()):
            param_values = '%s%s' % (param_values, params[k])

        # 生成签名
        signature = hmac.new(app_key, param_values, hashlib.sha256).hexdigest()
        params['signature'] = signature

        # 风控事件发送post请求
        url = url_risk
        headers = {'Content-Type': 'application/json', 'real-ip': '192.1.1.2'}
        # headers = {'Content-Type': 'application/json'}
        risk_request = urllib2.Request(url=url, headers=headers, data=json.dumps(params))
        # 获取返回json
        risk_response = urllib2.urlopen(risk_request)
        # 解析返回json
        risk_response_data = risk_response.read()
        # print risk_response_data
        # 添加检查点，请求成功返回的json中包含："info":"OK"  "status":"200"
        print cnt
        if "OK" and "200" in risk_response_data:
            print risk_response_data
            #             f.write(risk_response_data)
            #             f.write("\n********************RISK PASS********************")
            print "********************RISK PASS********************"
        else:
            print risk_response_data
            # f.write("\n********************RISK FAILED********************")
            print "********************RISK FAILED********************"

        t.sleep(10)
        # 上报事件
        url1 = url_report
        headers = {'Content-Type': 'application/json', 'real-ip': '192.1.1.2'}
        report_request = urllib2.Request(url=url1, headers=headers, data=json.dumps(params))
        report_response = urllib2.urlopen(report_request)
        report_response_data = report_response.read()
        # print report_response_data
        # 添加检查点，请求成功返回的json中包含："info":"OK"  "status":"200"
        if "OK" and "200" in risk_response_data:
            #             f.write("\n********************REPORT PASS********************")
            print "********************REPORT PASS********************"
        else:
            #             f.write("\n********************REPORT FAILED********************")
            print "********************REPORT FAILED********************"
            # t.sleep(1)

    print "END TIME IS: %s" % ctime()


if __name__ == '__main__':
    risk_report_all_sen()
