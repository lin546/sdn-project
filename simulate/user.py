"""
 @file     user.py                                                       
 @brief    本文件用于处理用户登录的验证，显示用户列表，实现用户的增删改                                                 
 Details.                                                                  
"""

import hashlib
from flask import Blueprint,request,session,render_template,url_for,redirect,g
from .utils.sqlhelper import sqlHelper
from simulate import gol

# 定义蓝图
bp_user = Blueprint('bp_user', __name__,template_folder='templates',static_folder='static')
user_dict = {}
#用户注册
@bp_user.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['pwd']
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        if error is None:
                m=hashlib.md5()
                m.update(password.encode('utf-8'))
                sql = "INSERT INTO user (uname, pwd) VALUES %s,%s"
                args = [username,m.hexdigest(),]        
                sqlHelper.add(sql,args)
        else:
            return redirect(url_for("bp_user.login"))
    return render_template('auth/register.html')

#用户登录
@bp_user.route('/login', methods=('GET','POST'))
def login():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['pwd']
        m=hashlib.md5()
        m.update(password.encode('utf-8'))
        error = None
        sql = "SELECT uname,root FROM user WHERE uname = %s and pwd = %s"
        args = [username,m.hexdigest(),]        
        user = sqlHelper.fetch_one(sql,args)
        if user is None:
            error = 'name or pwd error ！'
        if error is None:
            session.clear()
            session['user_name'] = user[0]
            session['root'] = user[1]
            return redirect(url_for('bp_index.index'))
        gol.userslog.info("用户登陆！！")
    return render_template('index.html')
 
#用户登出
@bp_user.route('/logout')
def logout():
    session.clear()
    gol.userslog.info("用户退出登录！！")
    return redirect(url_for('bp_user.login'))


# 用户列表
@bp_user.route('/users')
def user_manager():
    sql = "SELECT id,uname,pwd FROM user"
    users = sqlHelper.fetch_all(sql,None)
    user_dict.clear()
    for row in users:
      id = row[0]
      uname = row[1]
      password = row[2]
      dict = {}
      dict['id'] = id
      dict['uname'] = uname
      dict['pwd'] = password
      user_dict[id]=dict
    return render_template("user/users.html",users = user_dict)

# 修改密码
@bp_user.route('/modify-pwd',methods=('GET','POST'))
def modify_pwd():
    if request.method == 'POST':
        password = request.form['new_pwd']
        user_name = session.get('user_name')
        sql = "UPDATE user SET pwd = %s WHERE uname = %s"
        args = [password,user_name,]
        rowcount = sqlHelper.update(sql,args)
        gol.userslog.info("修改密码！！！！")
        return redirect(url_for('bp_user.login'))

# 删除用户
@bp_user.route('/delete/<uname>/',methods=('GET','POST'))
def del_user(uname):
    if request.method == 'GET':

        sql = "DELETE FROM user WHERE uname = %s"
        args = [uname,]
        rowcount = sqlHelper.delete(sql,args)
        gol.userslog.info("删除用户！！！！")
        return redirect(url_for('bp_user.user_manager',root1 = session.get('root')))
        #return redirect(url_for('bp_user.user_manager'))



# 添加用户
@bp_user.route('/add-user',methods=['GET','POST'])
def add_user():
    if request.method == 'POST':
        id = request.form['id']
        username = request.form['username']
        password = request.form['password']

        
        sql="select * from user where uname= %s"
        args = [username,]
        rowcount = sqlHelper.add(sql,args)
        if rowcount==1:
            return redirect(url_for('bp_user.user_manager',root1 = session.get('root')))

        m=hashlib.md5()
        m.update(password.encode('utf-8'))
        sql = "INSERT INTO user (id, uname, pwd, root) VALUES ( %s , %s , %s, 0)"
        args = [id,username,m.hexdigest(),]
        rowcount = sqlHelper.add(sql,args)

        gol.userslog.info("添加用户！！！！")
        return redirect(url_for('bp_user.user_manager',root1 = session.get('root')))

# 修改用户
@bp_user.route('/modify-user',methods=('GET','POST'))
def modify_user():
    if request.method == 'POST':
        id = request.form['id']
        username = request.form['username']
        password = request.form['password']

        sql="select * from user where uname= %s"
        args = [username,]
        rowcount = sqlHelper.add(sql,args)
        if rowcount==1:
            return redirect(url_for('bp_user.user_manager',root1 = session.get('root')))

        m=hashlib.md5()
        m.update(password.encode('utf-8'))
        sql = "UPDATE user SET uname = %s , pwd = %s WHERE id = %s"
        args = [username,m.hexdigest(),id]
        rowcount = sqlHelper.update(sql,args)
        return redirect(url_for('bp_user.user_manager',root1 = session.get('root')))


# 修改用户
@bp_user.route('/modify-user/<id>',methods=('GET','POST'))
def modify_user_byid(id):
    if request.method == 'GET':
        print("id:"+id)
        gol.userslog.info("修改用户:"+id)
        return render_template("user/modify-user.html",user_id = id)

@bp_user.before_app_request
def load_logged_in_user():
    user_name = session.get('user_name')
    if user_name is None:
        g.user = None
    else:
        sql =  'SELECT * FROM user WHERE id = %s'
        args = [user_name,]        
        sqlHelper.fetch_one(sql,args)