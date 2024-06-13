import uiautomator2 as u2
import time

def unlock_device(device):
    device.screen_on()  # 确保屏幕是打开的
    time.sleep(2)  # 等待屏幕亮起

    def is_screen_unlocked(device):
        return device.info.get("screenOn") and device.info.get("currentPackageName") != "com.android.systemui"

    if not is_screen_unlocked(device):
        print("解锁设备...")
        for _ in range(3):  # 尝试多次解锁
            device.swipe(0.5, 0.9, 0.5, 0.1)  # 从下往上滑动解锁
            time.sleep(2)  # 等待解锁操作完成
            if is_screen_unlocked(device):
                break
        else:
            print("解锁失败，设备可能已被锁定")
    else:
        print("设备已解锁")