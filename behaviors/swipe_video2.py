import random
import time

def swipe_videos2(device):
    total_watch_time = 0
    for i in range(1000):
        watch_time = random.randint(15, 40)
        print(f"设备 {device.serial} 正在观看视频，时长: {watch_time}秒")
        time.sleep(watch_time)
        total_watch_time += watch_time
        print(f"设备 {device.serial} 第 {i+1} 次滑动，总观看时长: {total_watch_time}秒")
        device.swipe(0.5, 0.8, 0.5, 0.2)
        time.sleep(2)  # 确保滑动完成