import streamlit as sl
import os, signal
from functions import write_txt, start_subprocess, driver_get, change_process_status
import subprocess
import psutil
from contextlib import suppress
import shutil

"""
# Welcome to Umiyuri Stepper.

"""

if not os.path.exists("info.txt"):
    with open("info.txt", "w") as f:
        f.write("\n")

a = sl.sidebar.text('Made by umiyurikaiteitan')

with open("info.txt", "r") as f:
    try:
        lines = f.readlines()
        username = lines[0].strip()
        password = lines[1].strip()
    except:
        username = ""
        password = ""
        write_txt(1, f"{username}\n{password}\n\n")

email = sl.text_input("Email", value=username)
password = sl.text_input("Password", value=password, type='password')

start = sl.button("Start")
if start:
    sl.success('Umiyuri Stepper started')
    write_txt(1, f"{email}\n")
    write_txt(2, f"{password}\n")
    write_txt(3, "running")
    with open("functions.py", 'r') as f:
        data = f.read()
        data = data.replace('###', 'options.add_argument("--headless")')
    with open("functions.py", 'w') as f:
        f.write(data)

    proc = start_subprocess("umiyuri.py")

start_browser = sl.button("Start with browser (no headless)")
if start_browser:
    sl.success('Umiyuri Stepper started')
    write_txt(1, f"{email}\n")
    write_txt(2, f"{password}\n")
    write_txt(3, "running")
    with open("functions.py", 'r') as f:
        data = f.read()
        data = data.replace('options.add_argument("--headless")', '###')
    with open("functions.py", 'w') as f:
        f.write(data)

    proc = start_subprocess("umiyuri.py")

pause = sl.button("Pause")
if pause:
    arr = [False]
    change_process_status(arr, 'pause')
    write_txt(3, "paused")
    sl.warning("Paused")
    print("Paused")

# enable resume button
resume = sl.button("Resume")
if resume:
    arr = [False]
    change_process_status(arr, 'resume')
    sl.success("Resumed")
    print("Resumed")
    write_txt(3, "running")


stop = sl.button("Stop")
if stop:
    arr = [False, False]
    change_process_status(arr, 'stop')
    # Clearing the Screen
    os.system('cls')


delete = sl.button('Delete items screenshots')
if delete:
    try:
        shutil.rmtree("pages/items/")
    except:
        pass
    sl.write("Items screenshots have been deleted.")