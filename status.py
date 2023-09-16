import string
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
    elif status == "running":
        return "running"
    elif status == "stop":
        return "stop"
    elif status == "captcha":
        return "captcha"
    else:
        print("Invalid status.")
        write_status_to_txt()
        return "stop"
    return "running"