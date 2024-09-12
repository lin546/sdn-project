"""
 @file     views.py                                                       
 @brief    本文件用于处理用户登录过程中界面的转换                                                   
 Details.                                                                  
"""

from flask import *
from HelloFlask import app,gol

@app.route('/')
def hello_world():
    return render_template('user/login.html') #用户登录页面

@app.route("/index<root1>")
def index(root1):
    if not session.get("user_name"):
      return redirect("/login")
    name = session.get('user_name')
    gol.userslog.info(name +" : 用户登录！！！！")
    #ctime,cname=gol.get_userslog();
    return render_template("index.html",root1 = root1)

