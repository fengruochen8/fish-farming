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

def unlock_device(device):
    logger.info("尝试解锁设备...")
    device.screen_on()
    time.sleep(2)  # 等待屏幕亮起

    for _ in  range(5):  # 尝试最多5次滑动解锁
        if device(resourceId="com.android.systemui:id/lock_icon").exists:
            logger.info("设备处于锁屏状态，尝试解锁...")
            device.swipe(0.5, 0.8, 0.5, 0.2)  # 滑动解锁
            time.sleep(1)
        else:
            logger.info("设备已解锁")
            break
    else:
        logger.warning("设备解锁失败")
    logger.info("解锁过程完成")
    sys.stdout.flush()  # 刷新标准输出
    sys.stderr.flush()  # 刷新标准错误