import uiautomator2 as u2
import time
import random
from behaviors import unlock_device, swipe_video, search_and_watch

def get_device_ids(file_path):
    with open(file_path, 'r') as file:
        device_ids = file.readlines()
    return [device_id.strip() for device_id in device_ids]

def main():
    device_ids = get_device_ids('devices.txt')

    for device_id in device_ids:
        print(f"处理设备: {device_id}")
        try:
            d = u2.connect(device_id)
            print(f"连接到设备: {device_id}")

            # 解锁设备
            unlock_device(d)

            # 启动抖音
            print("启动抖音...")
            d.app_start("com.ss.android.ugc.aweme")

            # 执行滑动观看视频操作
            swipe_video(d, num_swipes=5)

            # 执行搜索和观看操作
            search_and_watch(d, search_text="弹幕游戏")

        except Exception as e:
            print(f"设备 {device_id} 处理时发生错误: {e}")

if __name__ == "__main__":
    main()