import logging

def _init():
    global devices_stats
    global dpid
    dpid = '1'
    devices_stats={"vxlan":1,"vxlan11":1}  #表示设备状态，1为在线，0为离线
    # setup_logger('userslog', r'.\static\log\users.log')
    # setup_logger('ruleslog', r'.\static\log\rules.log')
    # setup_logger('deviceslog', r'.\static\log\devices.log')
    global userslog  #用户日志
    userslog= logging.getLogger('userslog')
    global ruleslog  #规则命中日志
    ruleslog= logging.getLogger('ruleslog')
    global deviceslog  #设备日志
    deviceslog= logging.getLogger('deviceslog')

def setup_logger(logger_name, log_file, level=logging.INFO):

    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='a')
    fileHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)

