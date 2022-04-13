import os
import threading
from config import Config
from monitor.run import run_monitor
from scheduler.run import run_scheduler
from utils.check_config import check_config
from version import APP_VERSION
from web.app import FlaskApp

if __name__ == "__main__":
    # 参数
    os.environ['TZ'] = 'Asia/Shanghai'
    print("配置文件地址：%s" % os.environ.get('NASTOOL_CONFIG'))
    print('NASTool 当前版本号：%s' % APP_VERSION)

    # 检查配置文件
    config = Config()
    if not check_config(config):
        quit()

    # 设置全局代理
    app_cfg = config.get_config('app')
    if app_cfg:
        proxies = app_cfg.get('proxies')
        if proxies:
            http_proxy = proxies.get('http')
            if http_proxy:
                os.environ['HTTP_PROXY'] = http_proxy
            https_proxy = proxies.get('https')
            if https_proxy:
                os.environ['HTTPS_PROXY'] = https_proxy

    # 启动进程
    print("开始启动进程...")

    # 启动定时服务
    scheduler = threading.Thread(target=run_scheduler)
    scheduler.setDaemon(False)
    scheduler.start()

    # 启动监控服务
    monitor = threading.Thread(target=run_monitor)
    monitor.setDaemon(False)
    monitor.start()

    # 启动主WEB服务
    FlaskApp().run_service()
