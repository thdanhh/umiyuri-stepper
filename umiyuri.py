import time
import os
import bypass_cf
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from action import attack, loot, step, item_check, exist_test
from functions import driver_get, status_check

def main():
    driver = driver_get()
    bypass_cf.bypass(driver)

    item_count = 0 # tracking the number of items found with the bot
    step_count = 0 # tracking the number of steps taken with the bot
    npc_count = 0 # tracking the number of NPC killed with the bot
    mat_count = 0 # tracking the number of materials looted with the bot

    while True:
        if not status_check():
            break
        # Start stepping
        print("Stepping...")
        print()
        
        if attack(driver): npc_count += 1
        if loot(driver): mat_count += 1
        if item_check(driver): item_count += 1
        if step(driver): step_count += 1
        exist_test(driver)

        print(f"{step_count} steps taken in current session!")
        print(f"{item_count} items found in current session!")
        print(f"{npc_count} NPC killed in current session!")
        print(f"{mat_count} materials looted in current session!")
        print()
        time.sleep(3)
    driver.quit()

if __name__ == '__main__':
#     try:
#         main()
#     except TimeoutException:
#         print("bypass unsuccessful, pls try again")
#     except:
#         pass

    main()