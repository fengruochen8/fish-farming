import uiautomator2 as u2
import time
import logging
import sys

def setup_logging():
    # 配置日志记录器
    app_log_formatter = logging.Formatter('%(asctime)s - %(message)s')

    # 文件处理器，记录日志到文件
    file_handler = logging.FileHandler('app.log')
    file_handler.setFormatter(app_log_formatter)
    file_handler.setLevel(logging.INFO)

    # 控制台处理器，记录日志到控制台
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(app_log_formatter)
    console_handler.setLevel(logging.INFO)

    # 应用日志记录器配置
    logger = logging.getLogger(__name__)
    logger.handlers = []  # 清空默认的日志处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)
    return logger

logger = setup_logging()

def open_tiktok(device):
    logger.info("启动抖音...")
    device.app_start("com.ss.android.ugc.aweme")
    time.sleep(5)  # 等待应用启动
    logger.info("抖音已启动")
    sys.stdout.flush()  # 刷新标准输出
    sys.stderr.flush()  # 刷新标准错误