import time
import logging
import random
import uiautomator2 as u2

def connect_device(device_id):
    device = u2.connect(device_id)
    return device

def unlock_device(device):
    device.screen_on()
    time.sleep(2)
    if not device.info.get('screenOn'):
        device.unlock()
    if not device.info.get('screenOn'):
        device.swipe(0.5, 0.9, 0.5, 0.1)
    time.sleep(1)

def open_tiktok(device):
    device.app_start("com.ss.android.ugc.aweme")
    time.sleep(5)

def swipe_videos2(device, stop_event, log_queue):
    unlock_device(device)
    open_tiktok(device)
    total_watch_time = 0
    for i in range(1000):
        if stop_event.is_set():
            log_queue.put(f"设备 {device.serial} 操作已停止")
            break
        watch_time = random.randint(15, 40)
        log_queue.put(f"设备 {device.serial} 正在观看第 {i+1} 个视频，观看时间: {watch_time} 秒，总观看时间: {total_watch_time + watch_time} 秒")
        time.sleep(watch_time)
        total_watch_time += watch_time
        device.swipe(0.5, 0.8, 0.5, 0.2)
        time.sleep(2)
    log_queue.put(f"设备 {device.serial} 完成观看，总观看时间: {total_watch_time} 秒")