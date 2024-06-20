import uiautomator2 as u2
import logging
from uiautomator2 import Direction

# 配置日志记录
logging.basicConfig(level=logging.INFO)

# 设备ID
DEVICE_SERIAL = "CYTOQKIJMN6XRODM"

def test_swipe(device_serial):
    try:
        logging.info(f"连接到设备 {device_serial}")
        device = u2.connect(device_serial)

        logging.info(f"设备 {device_serial} 连接成功，开始 swipe_ext 滑动测试")
        device.swipe_ext(Direction.FORWARD, scale=0.9)  # 使用 swipe_ext 函数进行滑动

        logging.info(f"设备 {device_serial} 滑动完成")

    except Exception as e:
        logging.error(f"处理设备 {device_serial} 时发生错误: {e}")

if __name__ == "__main__":
    test_swipe(DEVICE_SERIAL)