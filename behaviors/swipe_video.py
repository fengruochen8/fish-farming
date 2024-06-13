import time
import random

def swipe_video(device):
    print("滑动视频...")
    device.swipe(0.5, 0.8, 0.5, 0.2)
    time.sleep(random.randint(5, 10))
    check_and_exit_live(device)

def check_and_exit_live(device):
    if device(resourceId="com.ss.android.ugc.aweme:id/1b", index=1).exists:
        print("检测到直播间，退出...")
        device.xpath('//android.widget.Button[@index=5]').click()
        time.sleep(2)