import subprocess
import sys
import time
import random
import string
import psutil
from win10toast import ToastNotifier
from win11toast import toast
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from contextlib import suppress
import streamlit as sl
import os

def write_txt(file, line_count, content):
    with open(file, 'r') as f:
        lines = f.readlines()
    lines[line_count - 1] = content
    with open(file, "w") as f:
        f.writelines(lines)
    return content

def read_txt(file, line_count):
    line = ""
    count = 0
    with open(file, 'r') as f:
        while count < line_count:
            line = f.readline()
            count += 1
    print(line)
    return line.strip()

def timer(start_time):
    mins, secs = divmod(time.time() - start_time, 60) 
    hours, mins = divmod(mins, 60)
    print("Umiyuri Stepper has been running for %02d:%02d:%02d" % (hours, mins, secs))

@sl.cache_resource
def start_subprocess(file, args=""):
    print("starting subprocess")
    return subprocess.Popen(["python", file, args])

# @sl.cache_data
# def write_status():
#     write_txt(3, 'stop')
#     return False
