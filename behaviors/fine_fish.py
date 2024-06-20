import time
import random
import logging
import numpy as np
from paddleocr import PaddleOCR
from PIL import Image
import io
import uiautomator2 as u2
from uiautomator2 import Direction

# 初始化OCR
ocr = PaddleOCR(use_angle_cls=True, lang='ch')

def fine_fish(device, stop_event, update_recognition_count):
    video_count = 0
    total_watch_time = 0

    # 启动抖音应用
    logging.info(f"设备 {device.serial} 启动抖音应用")
    device.app_start("com.ss.android.ugc.aweme")
    time.sleep(5)  # 等待抖音启动

    while not stop_event.is_set():
        video_count += 1
        watch_time = random.randint(15, 35)
        total_watch_time += watch_time

        logging.info(
            f"设备 {device.serial} 正在观看第 {video_count} 个视频，观看时间: {watch_time} 秒，总观看时间: {total_watch_time} 秒")

        time.sleep(5)  # 先等待5秒再进行OCR识别

        logging.info("开始捕捉屏幕...")
        try:
            # 使用screencap命令直接保存截图到文件
            screenshot_file = f"/sdcard/{device.serial}_screenshot.png"
            local_screenshot_file = f"{device.serial}_screenshot.png"
            device.shell(f"screencap -p {screenshot_file}")
            device.pull(screenshot_file, local_screenshot_file)

            with open(local_screenshot_file, 'rb') as f:
                raw_screenshot = f.read()

            if raw_screenshot is None:
                raise ValueError(f"设备 {device.serial} 截图失败，screenshot 为 None")

            logging.debug(f"原始截图长度: {len(raw_screenshot)}")

            try:
                screenshot = Image.open(io.BytesIO(raw_screenshot)).convert("RGB")
            except Exception as e:
                logging.error(f"设备 {device.serial} 的图像转换失败: {e}")
                time.sleep(5)
                continue

            screenshot = np.array(screenshot)

            logging.info("屏幕捕捉成功")

            x1, y1 = 0, 200
            x2, y2 = screenshot.shape[1], 1200
            cropped_img = screenshot[y1:y2, x1:x2]

            result = ocr.ocr(cropped_img, cls=True)

            if not result or not result[0]:
                logging.warning(f"设备 {device.serial} OCR 结果为空或无效，跳过该次循环")
                device.swipe_ext(Direction.FORWARD, scale=0.9)  # 使用 swipe_ext 函数进行滑动
                time.sleep(watch_time)
                continue

            texts = [line[1][0] for line in result[0]]
            logging.info(f"OCR识别文本: {texts}")

            if any(keyword in text for text in texts for keyword in ["积分池", "羊羊对决", "召唤", "弹幕游戏", "互动游戏", "弹幕互动", "互动弹幕游戏", "推力", "连胜", "积分"]):
                logging.info(f"设备 {device.serial} 识别结果包含关键字，点击控件")
                update_recognition_count()
                time.sleep(random.randint(1, 3))  # 随机等待1-3秒后点击
                try:
                    device(resourceId="com.ss.android.ugc.aweme:id/ew5").click()
                except Exception as e:
                    logging.info(f"当前视频检测为“简易直播间”类型，稍后进入直播间，观看直播。")
                    try:
                        device.xpath('//*[@text="点击进入直播间"]').click()
                        time.sleep(random.randint(5, 10))  # 随机等待进入直播间

                        # 检测是否进入直播间
                        if device(resourceId="com.ss.android.ugc.aweme:id/f6f").exists:
                            logging.info(f"设备 {device.serial} 已进入直播间，开始点赞")
                            for _ in range(4):
                                device.click(371, 955)  # 点赞位置
                                time.sleep(0.5)
                                device.click(769, 1240)  # 点赞位置
                                time.sleep(0.5)

                            watch_time_live = random.randint(300, 600)  # 观看直播5-10分钟
                            logging.info(f"设备 {device.serial} 观看直播 {watch_time_live // 60} 分钟")
                            time.sleep(watch_time_live)

                            logging.info(f"设备 {device.serial} 退出直播间")
                            device(resourceId="com.ss.android.ugc.aweme:id/root").click()
                            device.swipe_ext(Direction.FORWARD, scale=0.9)  # 退出直播间后滑动一次
                        else:
                            logging.warning(f"设备 {device.serial} 未检测到进入直播间控件，继续滑动")
                    except Exception as inner_e:
                        logging.error(f"处理设备 {device.serial} 时发生错误: {inner_e}")

                time.sleep(random.randint(1, 3))  # 随机等待1-3秒后滑动
                device.swipe_ext(Direction.FORWARD, scale=0.9)
            else:
                logging.info(f"设备 {device.serial} 识别结果不包含关键字，继续滑动视频")
                device.swipe_ext(Direction.FORWARD, scale=0.9)

            time.sleep(watch_time)
            if stop_event.is_set():
                break
        except Exception as e:
            logging.error(f"处理设备 {device.serial} 时发生错误: {e}")
            time.sleep(5)

def swipe_videos(device, stop_event):
    video_count = 0
    total_watch_time = 0

    # 启动抖音应用
    logging.info(f"设备 {device.serial} 启动抖音应用")
    device.app_start("com.ss.android.ugc.aweme")
    time.sleep(5)  # 等待抖音启动

    while not stop_event.is_set():
        video_count += 1
        watch_time = random.randint(15, 35)
        total_watch_time += watch_time

        logging.info(
            f"设备 {device.serial} 正在观看第 {video_count} 个视频，观看时间: {watch_time} 秒，总观看时间: {total_watch_time} 秒")

        time.sleep(watch_time)
        device.swipe_ext(Direction.FORWARD, scale=0.9)  # 使用 swipe_ext 函数进行滑动
        if stop_event.is_set():
            break