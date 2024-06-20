import subprocess
import uiautomator2 as u2
import logging

def install_uiautomator(device_serial):
    # 使用最新的apk链接
    subprocess.run(f"adb -s {device_serial} uninstall com.github.uiautomator", shell=True)
    subprocess.run(f"adb -s {device_serial} uninstall com.github.uiautomator.test", shell=True)
    subprocess.run(f"adb -s {device_serial} install -r https://github.com/openatx/android-uiautomator-server/releases/download/v1.1.7/app-uiautomator.apk", shell=True)
    subprocess.run(f"adb -s {device_serial} install -r https://github.com/openatx/android-uiautomator-server/releases/download/v1.1.7/app-uiautomator-test.apk", shell=True)

def start_uiautomator(device_serial):
    # 启动 uiautomator 服务
    result = subprocess.run(f"adb -s {device_serial} shell am instrument -w com.github.uiautomator.test/androidx.test.runner.AndroidJUnitRunner", shell=True, capture_output=True, text=True)
    if "INSTRUMENTATION_STATUS: Error" in result.stderr:
        logging.error(f"设备 {device_serial} 启动 uiautomator 服务失败: {result.stderr}")
    else:
        logging.info(f"设备 {device_serial} 启动 uiautomator 服务成功")

def connect_device(device_serial):
    device = u2.connect(device_serial)
    return device

def initialize_device(device_serial):
    install_uiautomator(device_serial)
    start_uiautomator(device_serial)
    device = connect_device(device_serial)
    return device

def get_connected_devices():
    result = subprocess.run("adb devices", shell=True, capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")
    devices = [line.split("\t")[0] for line in lines if "\tdevice" in line]
    return devices