import time
import random

def watch_videos(device):
    for _ in range(5):
        print("滑动观看视频...")
        device.swipe(0.5, 0.8, 0.5, 0.2)
        time.sleep(random.randint(5, 10))

        # 检查是否在直播间
        if device(resourceId="com.ss.android.ugc.aweme:id/1b", index=1).exists:
            print("发现直播间，退出...")
            device.xpath('//android.widget.Button[@index=5]').click()
            time.sleep(2)