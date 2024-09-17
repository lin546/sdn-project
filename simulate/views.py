"""
 @file     views.py                                                       
 @brief    本文件用于处理用户登录过程中界面的转换                                                   
 Details.                                                                  
"""

from flask import *

# 定义蓝图
bp_index = Blueprint('bp_index', __name__,template_folder='templates',static_folder='static')

@bp_index.route('/')
def hello_world():
    return render_template('user/login.html') #用户登录页面

@bp_index.route("/index")
def index():
    from simulate import gol
    if not session.get("user_name"):
      return redirect("/login")
    name = session.get('user_name')
    isroot = session.get('root')
    gol.userslog.info(name +" : 用户登录！！！！")
    #ctime,cname=gol.get_userslog();
    return render_template("index.html",root1 = isroot)

