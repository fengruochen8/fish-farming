import cv2
import numpy as np
import uiautomator2 as u2
from paddleocr import PaddleOCR
import time
import logging
import random

# 初始化 PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='ch')


def ocr_screenshot(device):
    screenshot = device.screenshot(format='opencv')
    return screenshot


def process_ocr_result(result):
    keywords = ["积分池", "羊羊对决", "召唤", "弹幕游戏", "互动游戏", "弹幕互动", "互动弹幕游戏", "推力"]
    logging.info(f"OCR 结果: {result}")

    for line in result:
        text = line[1][0]
        logging.info(f"OCR识别文本: {text}")
        if any(keyword in text for keyword in keywords):
            return True
    return False


def fine_fish(device, stop_event):
    video_count = 0
    total_watch_time = 0

    while not stop_event.is_set():
        try:
            video_count += 1
            watch_time = random.randint(10, 15)
            total_watch_time += watch_time
            logging.info(
                f"设备 {device.serial} 正在观看第 {video_count} 个视频，观看时间: {watch_time} 秒，总观看时间: {total_watch_time} 秒")
            time.sleep(5)

            logging.info("开始截图...")
            screenshot = ocr_screenshot(device)
            logging.info("截图成功")

            result = ocr.ocr(screenshot, cls=True)
            logging.info("OCR识别完成")
            logging.info(f"OCR 结果: {result}")

            if process_ocr_result(result[0]):
                logging.info("识别结果包含关键字，点击控件")
                if device(resourceId="com.ss.android.ugc.aweme:id/ew5").exists:
                    device(resourceId="com.ss.android.ugc.aweme:id/ew5").click()
                    time.sleep(2)
                else:
                    logging.info("未找到控件，继续滑动视频")

                # 无论是否点击成功都需要立即滑动视频
                device.swipe_ext("up", 0.8)
            else:
                logging.info("识别结果不包含关键字，继续滑动视频")
                device.swipe_ext("up", 0.8)

            time.sleep(watch_time - 5)  # 扣除前面已经等待的5秒

        except Exception as e:
            logging.error(f"错误: {e}")

    logging.info(f"设备 {device.serial} 操作已停止")


def swipe_videos(device, stop_event):
    video_count = 0
    total_watch_time = 0

    while not stop_event.is_set():
        video_count += 1
        watch_time = random.randint(10, 15)
        total_watch_time += watch_time
        logging.info(
            f"设备 {device.serial} 正在观看第 {video_count} 个视频，观看时间: {watch_time} 秒，总观看时间: {total_watch_time} 秒")
        time.sleep(watch_time)
        device.swipe_ext("up", 0.8)

    logging.info(f"设备 {device.serial} 操作已停止")