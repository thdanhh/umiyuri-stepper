import subprocess
import sys
import time
import winsound
import random
import string
from win10toast import ToastNotifier
from win11toast import toast
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def driver_get():
    # Set up chrome driver
    options = ChromeOptions()
    options.add_argument('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36')
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

def start_subprocess(file):
    proc = subprocess.Popen(["python", file])
    return proc

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
    else:
        print("Invalid status. info.txt deleted")
        os.remove('info.txt')
        return False
    return True

def captcha(captcha_link):
    if captcha_link.is_displayed():
        print("Solve the captcha to continue, if you are done solving, type c to continue the loop.")
        alert_sound()
        toast("Verification Detected", "Solve the captcha to continue stepping")
        while True:
            if input().lower() == "c":
                break