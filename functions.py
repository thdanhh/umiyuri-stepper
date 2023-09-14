import subprocess
import sys
import time
import winsound
import random
import string
import psutil
from win10toast import ToastNotifier
from win11toast import toast
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from contextlib import suppress
import streamlit as sl

def driver_get():
    # Set up chrome driver
    # TODO: add feature to update chrome automatically
    print("initializing driver")
    options = ChromeOptions()
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--disable-popup-blocking')
    options.add_argument("--headless")
    options.add_argument("--test-type=webdriver")
    print("adding options argument")
    driver = Chrome(options=options)
    print("initialized driver successfully")
    return driver

def write_txt(line, content):
    lines = []
    with open("info.txt", 'r') as f:
        lines = f.readlines()
    lines[line - 1] = content
    with open("info.txt", "w") as f:
        f.writelines(lines)

def status_check():
    with open("info.txt", 'r') as f:
            lines = f.readlines()
            status = lines[2].strip()
    if status == "paused":
        print("Paused")
        while True:
            time.sleep(1)
            with open("info.txt", 'r') as f:
                lines = f.readlines()
                status = lines[2].strip()
            if status == "running":
                print("Resumed")
    elif status == "running":
        time.sleep(1)
    elif status == "stop":
        return False
    else:
        print("Invalid status. info.txt deleted")
        os.remove('info.txt')
        return False
    return True

@sl.cache_resource
def start_subprocess(file):
    print("starting subprocess")
    return subprocess.Popen(["python", file])

def captcha(captcha_link):
    if captcha_link.is_displayed():
        print("Solve the captcha to continue, if you are done solving, type c to continue the loop.")
        alert_sound()
        toast("Verification Detected", "Solve the captcha to continue stepping")
        while True:
            if input().lower() == "c":
                break

def change_process_status(arr, target_status):
    for process in psutil.process_iter():
        with suppress(psutil.NoSuchProcess):
            if process.name() == 'python.exe' and 'python umiyuri.py' in process.cmdline():
                if target_status == 'pause':
                    process.suspend()
                if target_status == 'resume':
                    process.resume()
                if target_status == 'stop':
                    process.kill()
                arr[0] = True

            if target_status == 'stop':
                if process.name() == 'chrome.exe' and ('--test-type=webdriver') in process.cmdline():
                    process.kill()
                    arr[1] = True

#             had_changed = True
#             for element in arr:
#                 if element is False:
#                     had_changed = False
#                     break
#             if had_changed is True:
#                 break
