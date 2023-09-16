import time
import os
import sys
import bypass_cf
from seleniumbase import Driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from action import attack, loot, step, item_check
from functions import timer
from status import status_check
from captcha import exist_test, delay_for_verification, notify_captcha

def main(driver, auto_open_captcha):
    bypass_cf.bypass(driver)

    item_count = 0 # tracking the number of items found with the bot
    step_count = 0 # tracking the number of steps taken with the bot
    npc_count = 0 # tracking the number of NPC killed with the bot
    mat_count = 0 # tracking the number of materials looted with the bot

    status = status_check()
    start_time = time.time()
    while status == "running":

        # Start stepping
        print("Stepping...")
        print()

        if loot(driver): mat_count += 1
        if attack(driver, auto_open_captcha): npc_count += 1
        if item_check(driver): item_count += 1
        if step(driver): step_count += 1

        print(f"{step_count} steps taken in current session!")
        print(f"{item_count} items found in current session!")
        print(f"{npc_count} NPC killed in current session!")
        print(f"{mat_count} materials looted in current session!")

        print()
        timer(start_time)

        print()
        delay_for_verification(time.time())

        captcha = None
        if exist_test(driver, 'step', captcha):
            notify_captcha(captcha, auto_open_captcha)

        status = status_check()
        if status == 'stop':
            break

if __name__ == '__main__':
    print('parsing arguments')
    option_headless = False
    auto_open_captcha = False
    argc = len(sys.argv)
    if argc > 1:
        for i in range(1, argc):
            if sys.argv[i] == "headless":
                option_headless = True
            if sys.argv[i] == "auto_open_captcha":
                auto_open_captcha = True


    undetected = False
    try_count = 0
    BYPASS_LIMIT = 3
    while not undetected and try_count < BYPASS_LIMIT:
        driver = Driver(uc=True, headless2=option_headless)
        try:
            main(driver, auto_open_captcha)
            undetected = True
        except TimeoutException:
            undetected = False
            print("bypass unsuccessful, closing and trying again")
            try_count += 1
            if try_count >= BYPASS_LIMIT:
                print("bypass took too many tries, ensure that you have a stable connection")
        finally:
            print("quiting driver")
            driver.quit()

    print("stopping script\n")