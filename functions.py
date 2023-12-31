import subprocess
import sys
import time
import random
import string
import psutil
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
    return line.strip()

def get_time_elapsed_from(start_time):
    return time.time() - start_time

def print_elapsed_time(elapsed_time):
    hours = int(elapsed_time/3600)
    mins = int((elapsed_time/60)%60)
    secs = int(elapsed_time%60)
    print("Umiyuri Stepper has been running for %02d:%02d:%02d" % (hours, mins, secs))

@sl.cache_resource
def start_subprocess(file, args=[]):
    print("starting subprocess")
    return subprocess.Popen(["python", file] + args)
