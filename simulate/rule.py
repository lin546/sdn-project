"""
 @file     rule.py                                                       
 @brief    本文件用于规则列表网页的转换，处理流表的增删查                                                 
 Details.                                                                  
"""

import requests,json
import hashlib
from flask import *
from .utils.sqlhelper import sqlHelper
from simulate import gol

# 定义蓝图
bp_rule = Blueprint('bp_rule', __name__,template_folder='templates')


@bp_rule.route('/rule-list')
def rule_list():
    from . import app
    remote_ip = app.config.get("IP")
    #dpid = nodes.get_dpid()
    url = remote_ip+"/stats/flow/"+gol.dpid

    response = requests.request("GET", url)
    data = json.loads(response.text)
    
    flow_entry = []
    flow_entry = data[gol.dpid]
    flow_entry_dict_item = {}
    flow_entry_list_item = []



    file = open("./simulate/static/log/rules.log", 'w').close()

    for item in flow_entry:
       matchDict={}
       actionsList=[]
       actionsDict={}

         #读取ovs的流表
       flow_entry_dict_item['dpid'] = gol.dpid
       flow_entry_dict_item['priority'] = item['priority']
       flow_entry_dict_item['idle_timeout'] = item['idle_timeout']
       flow_entry_dict_item['match'] = item['match']
       flow_entry_dict_item['actions'] = item['actions']
       if item['match']:
            flow_entry_dict_item['match_in_port'] = item['match']['in_port']
       flow_entry_dict_item['out_port'] = item['actions'][0]
       flow_entry_dict_item['packet_count'] = item['packet_count']
       flow_entry_dict_item['duration_sec'] = item['duration_sec']
       new_dict = flow_entry_dict_item.copy()
       flow_entry_list_item.append(new_dict)

       #将流表插入数据库
       priority = item['priority']
       idle_timeout = item['idle_timeout']
       matchDict = item['match']
       actionsDict['type'] = 'OUTPUT'
       actionsDict['port'] = new_dict['actions'][0].split(':')[1] 
       actionsList.append(actionsDict)
       payload_dict = {}
       payload_dict['dpid'] = gol.dpid
       payload_dict['priority'] = priority
       payload_dict['idle_timeout'] = idle_timeout
       payload_dict['match'] = matchDict
       payload_dict['actions'] = actionsList
       payload = json.dumps(payload_dict)

         #计算流表的hsah
       m=hashlib.md5()
       m.update('username'.encode('utf-8')) 
       m.update(payload.encode('utf-8'))

       name = session.get('user_name')
       sql = "INSERT IGNORE rules (hash,rule, uname) VALUES ( %s ,%s , %s ) "
       args = [m.hexdigest(),payload,name,]
       sqlHelper.add(sql,args)
       gol.ruleslog.info(payload+" 命中次数："+str(item['packet_count']))

    return render_template('rule/rule.html',r_flow_entry_list_item = flow_entry_list_item)


@bp_rule.route('/add-rule', methods=('GET','POST'))
def add_rule():
    if request.method == 'POST':
        from simulate import app
        remote_ip = app.config.get("IP")
        url = remote_ip+"/stats/flowentry/add"
        matchDict={}
        actionsList=[]
        dpid = app.config.get("DPID")
        idle_timeout = request.form['idle_timeout']#过时时间
        priority = request.form['priority']#优先
        type = request.form['type']#协议类型
        count = 0    #统计以下四个if的命中次数
        if type!= 'all':
            count=count+1
            matchDict['nw_proto']=type

        src_ip = request.form['src_ip']#源ip
        if src_ip!= 'None':
            count=count+1
            matchDict['nw_src']=src_ip

        dst_ip = request.form['dst_ip']#目的ip
        if dst_ip!= 'None':
            count=count+1
            matchDict['nw_dst']=dst_ip

        src_port = request.form['src_port']#源端口号
        if src_port!= 'None':
            count=count+1
            matchDict['tp_src']=src_port

        dst_port = request.form['dst_port']#目的端口号
        if dst_port!= 'None':
            count=count+1
            matchDict['tp_dst']=dst_port

        if count>0:
            matchDict['dl_type']=2048
        match_in_port = request.form['match_in_port']
        actions_out_port =request.form['actions_out_port']

        payload_dict = {}
        payload_dict['dpid'] = gol.dpid
        payload_dict['idle_timeout'] = int(idle_timeout)   
        payload_dict['priority'] = int(priority)

        matchDict['in_port']= int(match_in_port)
        payload_dict['match'] = matchDict

        actionsList.append({'type':'OUTPUT','port':actions_out_port})
        payload_dict['actions'] = actionsList

        payload = json.dumps(payload_dict)
        print(payload)
        
         
        m=hashlib.md5() #获取流表的hash
        m.update('username'.encode('utf-8')) 
        m.update(payload.encode('utf-8'))

          
        sql="select * from rules where hash= %s"  #向数据库查询流表是否已经存在
        args = [m.hexdigest(),]
        rowcount = sqlHelper.add(sql,args)
        print(rowcount)
        if rowcount == 1:
           return "failed"
        headers = {'user-agent': 'vscode-restclient'}
        response = requests.request("POST", url, data=payload, headers=headers)
        name = session.get('user_name')
        sql = "INSERT IGNORE rules (hash, rule, uname) VALUES ( %s ,%s , %s ) "
        args = [m.hexdigest(),payload,name,]

        sqlHelper.add(sql,args)
    gol.userslog.info(session.get('user_name')+"添加规则！！！！")
    return "ok"


@bp_rule.route('/deleterule/<dict_item>/', methods=('GET','POST'))
def delete_rule(dict_item):

    if request.method == 'GET':
        remote_ip = app.config.get("IP")
        url = remote_ip+"/stats/flowentry/delete_strict"

          #将获取到的流表字段进行拼接
        matchDict={}
        new_dict = {}
        actionsList=[]
        actionsDict={}
        #dpid = dict_item['dpid']
        new_dict = eval(dict_item)
        print(new_dict)
        priority = new_dict['priority']
        idle_timeout = new_dict['idle_timeout']
        matchDict = new_dict['match']
        actionsDict['type'] = 'OUTPUT'
        actionsDict['port'] = new_dict['actions'][0].split(':')[1]
        actionsList.append(actionsDict)
        payload_dict = {}
        payload_dict['dpid'] = gol.dpid
        payload_dict['priority'] = priority
        payload_dict['idle_timeout'] = idle_timeout
        payload_dict['match'] = matchDict
        payload_dict['actions'] = actionsList
        payload = json.dumps(payload_dict)
          #获取流表的hash
        m=hashlib.md5()
        m.update('username'.encode('utf-8')) 
        m.update(payload.encode('utf-8'))
        sql = "DELETE FROM rules WHERE hash = %s"
        args = [m.hexdigest()]
        print(m.hexdigest())
        rowcount = sqlHelper.delete(sql,args)
        headers = {'user-agent': 'vscode-restclient'}
        try:
            response = requests.request("POST", url, data=payload, headers=headers)
        except requests.exceptions.ConnectionError:
            print('Handle Exception')
    #return redirect(url_for('index',root1 = session.get('root')))
    return redirect(url_for('bp_rule.rule_list'))
