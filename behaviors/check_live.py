import uiautomator2 as u2

def check_and_exit_live(device):
    if device(resourceId="com.ss.android.ugc.aweme:id/1b", index=1).exists:
        print("检测到直播间，退出...")
        device.xpath('//android.widget.Button[@index="5"]').click()
    else:
        print("当前页面不是直播间，继续浏览...")