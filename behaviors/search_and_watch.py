import time
import random

def search_and_watch(device):
    print("点击搜索按钮...")
    device(resourceId="com.ss.android.ugc.aweme:id/content_container", index=0).click()
    time.sleep(2)

    print("聚焦到搜索窗口并输入文字‘弹幕游戏’...")
    device(resourceId="com.ss.android.ugc.aweme:id/et_search_kw").click()
    device.send_keys("弹幕游戏")
    device(description="搜索").click()
    time.sleep(5)  # 等待搜索结果加载

    for _ in range(random.randint(2, 3)):
        print("上滑搜索结果...")
        device.swipe(0.5, 0.8, 0.5, 0.2)
        time.sleep(5)

    for _ in range(5):
        print("查找并观看视频...")
        if device(resourceId="com.ss.android.ugc.aweme:id/lqy").exists:
            device(resourceId="com.ss.android.ugc.aweme:id/lqy").click()
            time.sleep(random.randint(5, 10))
            device(resourceId="com.ss.android.ugc.aweme:id/back_btn").click()
            time.sleep(2)

        for _ in range(random.randint(1, 3)):
            print("继续上滑搜索结果...")
            device.swipe(0.5, 0.8, 0.5, 0.2)
            time.sleep(5)

    print("查找直播并进入...")
    if device.xpath('//*[@text="直播"]').exists:
        device.xpath('//*[@text="直播"]').click()
        time.sleep(3)
        if device.xpath('//com.ss.android.ugc.aweme.xsearch.live.LynxSearchLive[@index=10]').exists:
            device.xpath('//com.ss.android.ugc.aweme.xsearch.live.LynxSearchLive[@index=10]').click()
            print("观看直播...")
            time.sleep(900)  # 观看15分钟