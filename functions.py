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
    options = ChromeOptions()
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36')
    options.add_argument('--disable-popup-blocking')
    ###
    options.add_argument("--test-type=webdriver")
    driver = Chrome(options=options)
    return driver

def write_txt(line, content):
    lines = []
    with open("info.txt", 'r') as f:
        lines = f.readlines()
    lines[line - 1] = content
    with open("info.txt", "w") as f:
        f.writelines(lines)

@sl.cache_resource
def start_subprocess(file):
    proc = subprocess.Popen(["python", file])
    return proc

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
            if process.name() == 'undetected_chromedriver.exe':
                if target_status == 'pause':
                    process.suspend()
                elif target_status == 'resume':
                    process.resume()
                elif target_status == 'stop':
                    process.kill()
                arr[0] = True

            if target_status == 'stop':
                if process.name() == 'chrome.exe' and ('--test-type=webdriver') in process.cmdline():
                    process.kill()
                    arr[1] = True

            had_changed = True
            for element in arr:
                if element is False:
                    had_changed = False
                    break
            if had_changed is True:
                break
