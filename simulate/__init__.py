"""
 @file     __init__.py                                                       
 @brief    本文件用与初始化系统，并建立与业务服务器端的通信                                                
 Details.                                                                  
"""
import socket
from flask import Flask
import logging
from logging.handlers import TimedRotatingFileHandler
from simulate import gol
from threading import Thread,Lock
import time

# 引入蓝图
from simulate.user import bp_user
from simulate.topology import bp_topology
from simulate.monitor import bp_monitor
from simulate.rule import bp_rule
from simulate.nodes import bp_nodes
from simulate.log import bp_log
from simulate.views import bp_index

# 引入配置文件
app = Flask(__name__)
app.config.from_pyfile('config/settings.cfg')

# 注册蓝图
app.register_blueprint(bp_user)
app.register_blueprint(bp_topology)
app.register_blueprint(bp_monitor)
app.register_blueprint(bp_rule)
app.register_blueprint(bp_nodes)
app.register_blueprint(bp_log)
app.register_blueprint(bp_index)

# 设置日志
formatter = logging.Formatter("[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s")
handler = TimedRotatingFileHandler("flask.log", when="D", interval=1, backupCount=15,encoding="UTF-8", delay=False, utc=True)
app.logger.addHandler(handler)
handler.setFormatter(formatter)

# 接受业务服务器的消息
def Recieve():
        address = ('82.157.0.86', 1241)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(address)
        while True:
           data, addr = s.recvfrom(2048)
           if not data:
                print("client has exist")
                break
           data = data.decode()
           print( "received:", data, "from", addr)
           if data in devices_stats_count.keys():
             lock.acquire()
             devices_stats_count[data] = 0
             gol.devices_stats[data] = 1
             lock.release()
        s.close()

# #对主机断开连接时间进行计算，超过15秒没有应答，即为断开连接
def Count():
    while True:
        for key in devices_stats_count:
            lock.acquire()
            devices_stats_count[key] += 1
            lock.release()   
            #print(devices_stats_count[key])
            if devices_stats_count[key] > 15:
                #print(key,"断开连接！！！！！！！")
                lock.acquire()
                gol.devices_stats[key] = 0
                lock.release()   
            time.sleep(1)

gol._init()
# 网络设备计数，value大于15默认为断开连接   
devices_stats_count={"vxlan0":0,"vxlan11":0}
lock = Lock()
t1 = Thread(target=Count)
t2 = Thread(target=Recieve)
t1.start()
t2.start() 


