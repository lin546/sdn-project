"""
 @file     log.py                                                       
 @brief    本文件用于日志网页的转换，包括用户日志，设备日志和规则匹配日志
           能够显示指定时间内的日志                                                  
 Details.                                                                  
"""

import time
from flask import *

# 定义蓝图
bp_log = Blueprint('bp_log', __name__,template_folder='templates')


 #用户登录登出日志
@bp_log.route('/user-log')
def user_log():
    return render_template('log/user_log.html')

@bp_log.route('/userslog/subtime', methods=['GET'])
def users_subtime():
    starttime = request.args.get("start")
    endtime = request.args.get("end") 
    file = "./sdn_simulate/static/log/users.log"
    t9 = time.strptime(starttime, '%Y-%m-%d')
    t11 = time.strptime(endtime, '%Y-%m-%d')
    data=''
    with open(file, 'r',encoding='utf-8') as f1:
       for line in f1:
          t = time.strptime(line[0:10], '%Y-%m-%d')  #前19个字符是时间字符串,取出并转成时间格式,用于比较时间
          if t >= t9 and t<=t11:  
              data=data + line + '<br/>'
    return str(data)

 #设备接入接出日志
@bp_log.route('/device-log')
def device_log():
    return render_template('log/device_log.html')

@bp_log.route('/deviceslog/subtime', methods=['GET'])
def devices_subtime():
    starttime = request.args.get("start")
    endtime = request.args.get("end") 
    file = './sdn_simulate/static/log/devices.log'
    t9 = time.strptime(starttime, '%Y-%m-%d')
    t11 = time.strptime(endtime, '%Y-%m-%d')
    data=''
    with open(file, 'r',encoding='utf-8') as f1:
       for line in f1:
          t = time.strptime(line[0:10], '%Y-%m-%d')  #前19个字符是时间字符串,取出并转成时间格式,用于比较时间
          if t >= t9 and t<=t11:  
              data=data + line + '<br/>'
    return str(data)

 #规则命中日志
@bp_log.route('/rule-log')
def rule_log():
    return render_template('log/rule_log.html')

@bp_log.route('/ruleslog/subtime', methods=['GET'])
def rules_subtime():
    starttime = request.args.get("start")
    endtime = request.args.get("end") 
    file = './sdn_simulate/static/log/rules.log'
    t9 = time.strptime(starttime, '%Y-%m-%d')
    t11 = time.strptime(endtime, '%Y-%m-%d')
    data=''
    with open(file, 'r',encoding='utf-8') as f1:
       for line in f1:
          t = time.strptime(line[0:10], '%Y-%m-%d')  #前19个字符是时间字符串,取出并转成时间格式,用于比较时间
          if t >= t9 and t<=t11:  
              data=data + line + '<br/>'
    return str(data)
