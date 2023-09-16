import string
import time
from functions import write_txt, read_txt

def read_status_from_txt():
    return read_txt("status.txt", 1)

def write_status_to_txt(status):
    return write_txt("status.txt", 1, status)

def status_check():
    status = read_status_from_txt()
    if status == "paused":
        print("Paused\n")
        while status == "paused":
            time.sleep(1)
            status = read_status_from_txt()
            if status != 'paused':
                break
    return status
