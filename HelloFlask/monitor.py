"""
 @file     monitor.py                                                       
 @brief    本文件用于资源监控网页的转换，显示服务器端实时cpu，内存和网速，处理系统的启停                                                  
 Details.                                                                  
"""

import pymysql,config,requests,json,time,psutil,os

from flask import *
from .utils.sqlhelper import sqlHelper

import platform
import datetime
from HelloFlask import app
from pyecharts.globals import CurrentConfig
from pyecharts import options as opts
from pyecharts.charts import Line

# 定义蓝图

bp_monitor = Blueprint('bp_monitor', __name__,template_folder='templates')


#资源监控页面
@bp_monitor.route('/mon')
def monitor():
    return render_template('monitor.html'); 


#获取服务器cpu、内存、网速信息
@bp_monitor.route('/GetPie')
def GetPie():
    try:
        cpuPercent = psutil.cpu_percent(0.5)        #cpu使用率
        m = psutil.virtual_memory()          #内存信息
        memoryTotal = round(m.total, 2) #总内存
        memoryUsed = round(m.used/m.total, 2)*100   #已用内存
        #网速
        net = psutil.net_io_counters()  
        bytesRcvd = (net.bytes_recv / 1024)
        bytesSent = (net.bytes_sent / 1024)
        time.sleep(0.2)
        net = psutil.net_io_counters()  
        newBytesRcvd = (net.bytes_recv / 1024)
        newBytesSent = (net.bytes_sent / 1024)
        realTimeRcvd = round((newBytesRcvd - bytesRcvd)*5,2)
        realTimeSent = round((newBytesSent - bytesSent)*5,2)
        tim = time.strftime('%H:%M:%S',time.localtime())   #当前时间
 
        resJson = []
        resJson.append({
                'time':tim,
                'json':{'Pvalue':cpuPercent},
                'pieBox':'CPU',

            })
        resJson.append(
            {
                'time':tim,
                'json':{'Pvalue':memoryUsed},
                'pieBox':'Memory',
            })

        resJson.append(
            {
                'time':tim,
                'json':{'Pvalue':realTimeRcvd,'Fvalue':realTimeSent},
                'pieBox':'IO',
            })
    except Exception as e:
        return json.dumps({'resultCode':1,'result':str(e)})
    else:
        return json.dumps({'resultCode':0,'result':resJson})


# 停止交换机运行
@bp_monitor.route('/sys/stop')
def sys_stop():
    os.system('~/stop.sh')
    return "ok"


# 启动交换机运行
@bp_monitor.route('/sys/start')
def sys_start():
    remote_ip = app.config.get("IP")
    url = remote_ip+"/stats/flowentry/add"
    os.system("gnome-terminal -e 'bash -c \"~/start.sh\"'")
    #os.system('~/start.sh')
    res = os.popen('~/aaa.sh')
    req_list = []#请求列表
    sql = "SELECT rule FROM rules"
    if res.read().find('true')>0:
        res.close()
        ruleslist = sqlHelper.fetch_all(sql,None)  
        print(ruleslist)
        for row in ruleslist:
               rule = {}
               rule = row[0]
               print(rule)
               req_list.append(grequests.post(url, data = rule))    
        res_list = grequests.map(req_list)
        return "ok"

    else:
        while 1:
           time.sleep(2)
           res = os.popen('~/aaa.sh')
           if res.read().find('true')>0:
               res.close()
               ruleslist = sqlHelper.fetch_all(sql,None)  
               print(ruleslist)
               for row in ruleslist:
                  rule = {}
                  rule = row[0]
                  print(rule)
                  req_list.append(grequests.post(url, data = rule))    
               res_list = grequests.map(req_list)
               break
           return "ok"
