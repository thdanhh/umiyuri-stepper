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
import os


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
        try:
            status = lines[2].strip()
        except:
            status = 'stop'
    if status == "paused":
        print("Paused\n")
        while status == "paused":
            time.sleep(1)
            with open("info.txt", 'r') as f:
                lines = f.readlines()
                status = lines[2].strip()
            if status != 'paused':
                break
    elif status == "running":
        return "running"
    elif status == "stop":
        return "stop"
    elif status == "captcha":
        return "captcha"
    else:
        print("Invalid status.")
        write_txt(3, "stop")
        return "stop"
    return "running"

@sl.cache_resource
def start_subprocess(file, args=""):
    print("starting subprocess")
    return subprocess.Popen(["python", file, args])

@sl.cache_data
def write_status():
    write_txt(3, 'stop')
    return False
