"""
 @file     nodes.py                                                       
 @brief    本文件用于处理ovs交换机和网络节点网页的转换，并显示其具体信息                                                
 Details.                                                                  
"""

import requests,json
from flask import *

from simulate import gol

# 定义蓝图
bp_nodes = Blueprint('bp_nodes', __name__,template_folder='templates')


# 获取OVS交换机DPID
def get_dpid():
    from simulate import app
    remote_ip = app.config.get("IP")
    url = url = remote_ip+"/stats/switches"
    headers = {'user-agent': 'vscode-restclient'}

    response = requests.request("GET", url, headers=headers)
    json_data = json.loads(response.text)

    
    return str(json_data[0])

# 获取交换机信息
@bp_nodes.route('/stats/desc')
def get_stats_desc():
    from simulate import app
    remote_ip = app.config.get("IP")
    gol.dpid = get_dpid()
    url = remote_ip+"/stats/desc/"+gol.dpid
    headers = {'user-agent': 'vscode-rest client'}
    response = requests.request("GET", url, headers=headers)
    json_data = json.loads(response.text)
    return render_template('nodes/switchs.html',switch_list = json_data)

# 获取交换机端口信息
@bp_nodes.route('/stats/portdesc/')
def get_stats_portdesc():
    from simulate import app
    remote_ip = app.config.get("IP")
    gol.dpid = get_dpid()
    url = remote_ip+"/stats/portdesc/"+gol.dpid
    headers = {'user-agent': 'vscode-restclient'}
    response = requests.request("GET", url, headers=headers)
    json_data = json.loads(response.text)   
    return render_template('nodes/hosts.html',host_list = json_data)

#获取主机的端口号
@bp_nodes.route('/portvalue')
def get_stats_port():
    from simulate import app
    remote_ip = app.config.get("IP")
    gol.dpid = get_dpid()
    url = remote_ip+"/stats/portdesc/"+gol.dpid
    headers = {'user-agent': 'vscode-restclient'}
    response = requests.request("GET", url, headers=headers)
    json_data = json.loads(response.text)   
    #host_value = json.dumps(json_data)
    print(type(json_data))
    hostList = []
    hostList = json_data[gol.dpid]
    for dict in hostList:
        gol.host_port.append(dict['port_no'])
    return str(gol.host_port)
