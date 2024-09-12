"""
 @file     topology.py                                                       
 @brief    本文件用于实现网络拓扑页面的转换，查询网络节点的信息，并返回给前端                                                 
 Details.                                                                  
"""

import requests,json
from HelloFlask import gol
from HelloFlask import app
from flask import Blueprint,render_template


# 定义蓝图
bp_topology = Blueprint('bp_topology', __name__,template_folder='templates')


@bp_topology.route('/topo')
def topology():
    return render_template('topology.html');


#接收前端发来的生成拓扑图的请求，向ryu控制器请求节点信息，将请求到的信息处理后返回给前端
@bp_topology.route('/data-server')
def data():
       remote_ip = app.config.get("IP")
       #url=remote_ip+"/stats/portdesc/223073848056654"
       req=requests.get(remote_ip+"/stats/portdesc/"+gol.dpid, timeout=(3,20))
       #result = json.loads(req.text)
       load_dict = json.loads(req.text)  #请求后的json数据转为字典

       ovsList=list(load_dict.keys())    
       ovsID = ovsList[0]      #获取交换机的datapathid
       portDict={}
       nodesList=[{'name':'ovs','x':0,'y':0,'id':ovsID}] #定义拓扑图节点列表
       edgesList=[]    #定义拓扑图的边列表

       nodeCount = 0  #主机节点个数
       count = 0      #总结点个数
       serCount = 0   #服务器节点个数

       for dictMsg in load_dict[ovsID]:
          if dictMsg['port_no']=="LOCAL":
               continue 
          if "vxlan" in dictMsg['name']:
              if gol.devices_stats[dictMsg['name']]==0:
                gol.deviceslog.info(dictMsg['name']+"断开连接！！！！！！")
                nodeDict={'name':dictMsg['name'],'x':150*serCount-200,'y':-100,'id':count+1,'addr':dictMsg['hw_addr'],'stat':0}
                edgeDict={'name':'vxlan','from':ovsID,'to':count+1}
              else:
                gol.deviceslog.info(dictMsg['name']+"已连接！！！！！！")
                nodeDict={'name':dictMsg['name'],'x':150*serCount-200,'y':-100,'id':count+1,'addr':dictMsg['hw_addr'],'stat':1}
                edgeDict={'name':'vxlan','from':ovsID,'to':count+1}
              serCount=serCount+1
          else:
              nodeDict={'name':dictMsg['name'],'x':150*nodeCount-200,'y':100,'id':count+1,'addr':dictMsg['hw_addr']}
              edgeDict={'name':None,'from':ovsID,'to':count+1}
              nodeCount=nodeCount+1
          count=count+1
          nodesList.append(nodeDict)
          edgesList.append(edgeDict)
       portDict={'nodes':nodesList,'edges':edgesList}
       jsonMsg=json.dumps(portDict)
       return jsonMsg