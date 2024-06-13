import time

import uiautomator2 as u2

def open_tiktok(device):
    print("启动抖音...")
    device.app_start("com.ss.android.ugc.aweme")  # 启动抖音
    time.sleep(10)  # 等待应用启动