import tkinter as tk
from tkinter import scrolledtext
from threading import Thread, Event
import time
import random
import logging
import queue
import uiautomator2 as u2
import subprocess

# 设置日志
log_queue = queue.Queue()

class QueueHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(self.format(record))

log_handler = QueueHandler(log_queue)
logging.basicConfig(level=logging.INFO, handlers=[log_handler], format='%(asctime)s - %(message)s')

class DeviceManager:
    def __init__(self):
        self.devices = []
        self.device_status = {}

    def update_device_list(self):
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
        device_ids = [line.split()[0] for line in result.stdout.splitlines() if line.endswith("device")]

        self.devices = []
        self.device_status = {}

        for device_id in device_ids:
            try:
                device = u2.connect(device_id)
                self.devices.append(device)
                self.device_status[device_id] = True
            except u2.exceptions.ConnectError:
                self.device_status[device_id] = False

    def get_connected_devices(self):
        return [device for device in self.devices if self.device_status[device.serial]]

device_manager = DeviceManager()

stop_event = Event()

def unlock_device(device):
    device.screen_on()
    time.sleep(2)
    if not device.info.get('screenOn'):
        device.unlock()
    if not device.info.get('screenOn'):
        device.swipe(0.5, 0.9, 0.5, 0.1)
    time.sleep(1)

def open_tiktok(device):
    device.app_start("com.ss.android.ugc.aweme")
    time.sleep(5)

def swipe_videos(device, stop_event):
    unlock_device(device)
    open_tiktok(device)
    total_watch_time = 0
    for i in range(1000):
        if stop_event.is_set():
            logging.info(f"设备 {device.serial} 操作已停止")
            break
        watch_time = random.randint(15, 40)
        logging.info(f"设备 {device.serial} 正在观看第 {i+1} 个视频，观看时间: {watch_time} 秒，总观看时间: {total_watch_time + watch_time} 秒")
        time.sleep(watch_time)
        total_watch_time += watch_time
        device.swipe(0.5, 0.8, 0.5, 0.2)
        time.sleep(2)
    logging.info(f"设备 {device.serial} 完成观看，总观看时间: {total_watch_time} 秒")

def start_operation():
    device_manager.update_device_list()
    devices = device_manager.get_connected_devices()
    if not devices:
        logging.info("没有连接的设备")
        return

    stop_event.clear()
    threads = []
    for device in devices:
        t = Thread(target=swipe_videos, args=(device, stop_event))
        t.start()
        threads.append(t)

def stop_operation():
    stop_event.set()

def update_log():
    while not log_queue.empty():
        log_text.config(state=tk.NORMAL)
        log_text.insert(tk.END, log_queue.get() + '\n')
        log_text.config(state=tk.DISABLED)
        log_text.yview(tk.END)
    log_text.after(1000, update_log)

# 创建GUI
root = tk.Tk()
root.title("抖音自动操作")

start_button = tk.Button(root, text="开始", command=lambda: Thread(target=start_operation).start())
start_button.pack(pady=5)

stop_button = tk.Button(root, text="停止", command=stop_operation)
stop_button.pack(pady=5)

log_text = scrolledtext.ScrolledText(root, width=80, height=20)
log_text.pack(pady=10)
log_text.config(state=tk.DISABLED)

update_log()

root.mainloop()