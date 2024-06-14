import uiautomator2 as u2
import time
import random
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


def swipe_videos2(device, stop_event):
    start_time = time.time()
    swipe_count = 0

    while not stop_event.is_set() and swipe_count < 1000:
        watch_time = random.randint(15, 40)
        logger.info(f"设备 {device.serial} 正在观看视频，观看时长: {watch_time} 秒")
        time.sleep(watch_time)

        swipe_count += 1
        total_watch_time = int(time.time() - start_time)
        logger.info(f"设备 {device.serial} 滑动次数: {swipe_count}，总观看时长: {total_watch_time} 秒")

        device.swipe(0.5, 0.8, 0.5, 0.2)  # 滑动
        time.sleep(2)  # 等待滑动完成
        sys.stdout.flush()  # 刷新标准输出
        sys.stderr.flush()  # 刷新标准错误