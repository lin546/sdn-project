"""
 @file     runserver.py                                                       
 @brief    本文件用于启动网页服务                                                 
 Details.                                                                  
"""


from simulate import app

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 5555

    app.run(HOST, PORT)

