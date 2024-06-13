# -*- coding: utf-8 -*-
import threading
import time
import uiautomator2 as u2
from behaviors.unlock_device import unlock_device
from behaviors.open_tiktok import open_tiktok
from behaviors.swipe_video2 import swipe_videos2

def handle_device(device_info):
    device_id, phone_number = device_info.split()
    print(f"处理设备: {device_id} ({phone_number})")
    try:
        d = u2.connect(device_id)
        print(f"连接到设备: {device_id} ({phone_number})")
        unlock_device(d)
        open_tiktok(d)
        swipe_videos2(d)
    except Exception as e:
        print(f"设备 {device_id} 处理时发生错误: {e}")

def main():
    with open("devices.txt", "r") as file:
        device_infos = [line.strip() for line in file.readlines()]

    threads = []
    for device_info in device_infos:
        thread = threading.Thread(target=handle_device, args=(device_info,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()