from flask import Flask, render_template, request, redirect, url_for, jsonify
import threading
import time
import uiautomator2 as u2
from behaviors.unlock_device import unlock_device
from behaviors.open_tiktok import open_tiktok
from behaviors.swipe_video2 import swipe_videos2
import logging
import sys

app = Flask(__name__)

def setup_logging():
    # 配置日志记录器
    app_log_formatter = logging.Formatter('%(asctime)s - %(message)s')

    # 文件处理器，记录日志到文件
    file_handler = logging.FileHandler('app.log')
    file_handler.setFormatter(app_log_formatter)
    file_handler.setLevel(logging.INFO)

    # 控制台处理器，记录日志到控制台
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(app_log_formatter)
    console_handler.setLevel(logging.INFO)

    # 应用日志记录器配置
    app.logger.handlers = []  # 清空Flask默认的日志处理器
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)

    # 禁用Werkzeug日志
    log = logging.getLogger('werkzeug')
    log.disabled = True

setup_logging()

# 存储线程和停止事件以便控制
threads = []
stop_events = []

def handle_device(device_info, stop_event):
    device_id, phone_number = device_info.split()
    app.logger.info(f"处理设备: {device_id} ({phone_number})")
    try:
        d = u2.connect(device_id)
        app.logger.info(f"连接到设备: {device_id} ({phone_number})")
        unlock_device(d)
        open_tiktok(d)
        swipe_videos2(d, stop_event)
    except Exception as e:
        app.logger.error(f"设备 {device_id} 处理时发生错误: {e}")
    finally:
        sys.stdout.flush()  # 刷新标准输出
        sys.stderr.flush()  # 刷新标准错误

def start_scripts():
    global threads, stop_events

    # 清空日志文件
    open('app.log', 'w').close()

    stop_events = []
    with open("devices.txt", "r") as file:
        device_infos = [line.strip() for line in file.readlines()]

    threads = []
    for device_info in device_infos:
        stop_event = threading.Event()
        stop_events.append(stop_event)
        thread = threading.Thread(target=handle_device, args=(device_info, stop_event))
        threads.append(thread)
        thread.daemon = True  # 设置守护线程
        thread.start()

def stop_scripts():
    global stop_events
    for stop_event in stop_events:
        stop_event.set()
    for thread in threads:
        if thread.is_alive():
            thread.join()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    start_scripts()
    return redirect(url_for('index'))

@app.route('/stop', methods=['POST'])
def stop():
    stop_scripts()
    return redirect(url_for('index'))

@app.route('/logs')
def logs():
    with open('app.log', 'r') as file:
        log_data = file.read()
    # 过滤掉包含 "GET /logs HTTP/1.1" 的行
    log_data = '\n'.join([line for line in log_data.split('\n') if "GET /logs HTTP/1.1" not in line])
    return jsonify(log_data.split('\n'))

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=5500, debug=True, use_reloader=False)
    except Exception as e:
        app.logger.error(f"Flask 应用程序发生错误: {e}")
        sys.exit(1)