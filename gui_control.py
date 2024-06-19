import tkinter as tk
from tkinter import scrolledtext
from threading import Thread, Event
import logging
import queue
import subprocess
import uiautomator2 as u2
from behaviors.fine_fish import fine_fish, swipe_videos

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
threads = []

def start_operation():
    device_manager.update_device_list()
    devices = device_manager.get_connected_devices()
    if not devices:
        logging.info("没有连接的设备")
        return

    logging.info(f"当前连接的设备数量: {len(devices)}")
    for device in devices:
        logging.info(f"设备ID: {device.serial}")

    stop_event.clear()
    global threads
    threads = []
    for device in devices:
        if fine_fish_flag.get():
            t = Thread(target=fine_fish, args=(device, stop_event, update_recognition_count))
        else:
            t = Thread(target=swipe_videos, args=(device, stop_event))
        t.start()
        threads.append(t)

def stop_operation():
    stop_event.set()
    for thread in threads:
        if thread.is_alive():
            thread.join()
    logging.info("停止按钮被点击，所有操作已终止")

def update_recognition_count():
    global recognition_count
    recognition_count += 1
    recognition_count_label.config(text=f"识别成功次数: {recognition_count}")

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

recognition_count = 0
recognition_count_label = tk.Label(root, text=f"识别成功次数: {recognition_count}")
recognition_count_label.pack(pady=5)

start_button = tk.Button(root, text="开始", command=lambda: Thread(target=start_operation).start())
start_button.pack(pady=5)

stop_button = tk.Button(root, text="停止", command=lambda: Thread(target=stop_operation).start())
stop_button.pack(pady=5)

fine_fish_flag = tk.BooleanVar()
fine_fish_checkbox = tk.Checkbutton(root, text="精细化养鱼", variable=fine_fish_flag)
fine_fish_checkbox.pack(pady=5)

log_text = scrolledtext.ScrolledText(root, width=80, height=20)
log_text.pack(pady=10)
log_text.config(state=tk.DISABLED)

update_log()

root.mainloop()