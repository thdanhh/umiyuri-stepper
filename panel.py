import streamlit as sl
import os, signal
from functions import write_txt, start_subprocess
import subprocess
import psutil
from contextlib import suppress
import shutil
from status import read_status_from_txt, write_status_to_txt
from functions import write_txt, read_txt

"""
# Welcome to Umiyuri Stepper.

"""

if not os.path.exists("info.txt"):
    with open("info.txt", "w") as f:
        f.write('\n' + '\n' + '\n')

if not os.path.exists("status.txt"):
    with open("status.txt", "w") as f:
        f.write('stop')

a = sl.sidebar.text('Made by umiyurikaiteitan')

username = read_txt("info.txt", 1)
password = read_txt("info.txt", 2)

email = sl.text_input("Email", value=username)
password = sl.text_input("Password", value=password, type='password')

start = sl.button("Start")
start_debug = sl.button("Start (debug)")
auto_open_captcha = sl.checkbox("Open verify page automatically (stop bot to take effect)")
pause = sl.button("Pause")
resume = sl.button("Resume")
stop = sl.button("Stop")
delete = sl.button('Delete items screenshots')

# if 'first_run' not in sl.session_state:
#     sl.session_state['first_run'] = True
#
# if sl.session_state['first_run'] is True:
#     sl.session_state['first_run'] = write_status_to_txt('stop')

if read_status_from_txt() != 'captcha':
    args = []
    if auto_open_captcha:
        args.append("auto_open_captcha")

    if start:
        write_txt("info.txt", 1, f"{email}\n")
        write_txt("info.txt", 2, f"{password}\n")
        write_status_to_txt('running')

        args.append("headless")

        proc = start_subprocess("umiyuri.py", args=args)
        sl.success('Umiyuri Stepper started')

    if start_debug:
        write_txt("info.txt", 1, f"{email}\n")
        write_txt("info.txt", 2, f"{password}\n")
        write_status_to_txt('running')

        proc = start_subprocess("umiyuri.py", args=args)
        sl.success('Umiyuri Stepper started')

    if resume:
        write_status_to_txt('running')
        sl.success("Resumed")
        print("Resume initiated\n")

    if pause:
        write_status_to_txt('paused')
        sl.warning("Paused")
        print("Pause initiated, waiting for current action to finish\n")

if stop:
    start_subprocess.clear()

    sl.error("Stopped")
    print("Stop initiated\n")
    write_status_to_txt('stop')

if delete:
    try:
        shutil.rmtree("pages/items/")
    except:
        pass
    sl.write("Items screenshots have been deleted.")