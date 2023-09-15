import time
import os
import sys
import bypass_cf
from seleniumbase import Driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from action import attack, loot, step, item_check, exist_test, delay_for_verification
from functions import status_check, timer

def main(driver):
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
        if attack(driver): npc_count += 1
        if item_check(driver): item_count += 1
        if step(driver): step_count += 1

        print(f"{step_count} steps taken in current session!")
        print(f"{item_count} items found in current session!")
        print(f"{npc_count} NPC killed in current session!")
        print(f"{mat_count} materials looted in current session!")
        timer(start_time)
        print()

        print("Checking for verification...\n")
        exist_test(driver, 'step')
        
        status = status_check()
        if status == 'stop':
            break
        delay_for_verification(time.time())

if __name__ == '__main__':
    option_headless = False
    if len(sys.argv[1]) > 1:
        option_headless = True

    undetected = False
    while not undetected:
        driver = Driver(uc=True, headless2=option_headless)
        try:
            main(driver)
            undetected = True
        except TimeoutException:
            undetected = False
            print("bypass unsuccessful, closing and trying again")
        finally:
            driver.quit()
            print("Quited driver")

    print("Stopped script")