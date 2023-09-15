import streamlit as sl
import os, signal
from functions import write_txt, write_status, start_subprocess, status_check
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

start_browser = sl.button("Start")
start = sl.button("Start headless (no browser)")
pause = sl.button("Pause")
resume = sl.button("Resume")

if 'first_run' not in sl.session_state:
    sl.session_state['first_run'] = True

if sl.session_state['first_run'] is True:
    sl.session_state['first_run'] = write_status()

with open("info.txt", 'r') as f:
    lines = f.readlines()
    try:
        status = lines[2].strip()
    except:
        status = 'stop'

if status == 'captcha':
    pass
else:
    if start:
        write_txt(1, f"{email}\n")
        write_txt(2, f"{password}\n")
        write_txt(3, "running")

        proc = start_subprocess("umiyuri.py", args="headless")
        sl.success('Umiyuri Stepper started')

    if start_browser:
        write_txt(1, f"{email}\n")
        write_txt(2, f"{password}\n")
        write_txt(3, "running")

        proc = start_subprocess("umiyuri.py")
        sl.success('Umiyuri Stepper started')

    if resume:
        write_txt(3, "running")
        sl.success("Resumed")
        print("Resume initiated\n")

    if pause:
        write_txt(3, "paused")
        sl.warning("Paused")
        print("Pause initiated, waiting for current action to finish\n")


stop = sl.button("Stop")
if stop:
    start_subprocess.clear()

    sl.error("Stopped")
    print("Stop initiated\n")
    write_txt(3, "stop")


delete = sl.button('Delete items screenshots')
if delete:
    try:
        shutil.rmtree("pages/items/")
    except:
        pass
    sl.write("Items screenshots have been deleted.")