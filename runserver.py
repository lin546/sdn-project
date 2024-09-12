"""
 @file     runserver.py                                                       
 @brief    本文件用于启动网页服务                                                 
 Details.                                                                  
"""


import os
from sdn_simulate import app

if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')

    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    app.run(HOST, PORT)

