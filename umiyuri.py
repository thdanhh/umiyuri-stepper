import time
import os
import sys
from seleniumbase import Driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException

from spend import EnergyQuestPointsManager
import bypass_cf
import action
from functions import get_time_elapsed_from, print_elapsed_time
from status import status_check, check_for_stop
from captcha import CaptchaHandler

class UmiyuriStepper():
    # Predefined methods
    bypass = bypass_cf.bypass

    attack = action.attack
    find_enemy_while_stepping = action.find_enemy_while_stepping
    loot = action.loot
    step = action.step
    item_check = action.item_check

    open_in_new_tab = action.open_in_new_tab

    def parse_arguments(self):
        print('parsing arguments')
        self.option_headless = False
        self.auto_open_captcha = False
        argc = len(sys.argv)
        if argc > 1:
            for i in range(1, argc):
                if sys.argv[i] == "headless":
                    self.option_headless = True
                if sys.argv[i] == "auto_open_captcha":
                    self.auto_open_captcha = True

    def main(self):
        self.parse_arguments()
        undetected = False
        try_count = 0
        BYPASS_LIMIT = 3
        while not undetected and try_count < BYPASS_LIMIT and status_check() != 'stop':
            try:
                self.run_driver()
                undetected = True
            except TimeoutException as timeout_err:
                if timeout_err.msg == "Bypass failed":
                    undetected = False
                    print("bypass unsuccessful, quiting driver and trying again")

                    try_count += 1
                    if try_count >= BYPASS_LIMIT:
                        print("bypass took too many tries, ensure that you have a stable connection")
                        break
                else:
                    self.driver.save_screenshot("screenshot.png")
                    raise
            except:
                self.driver.save_screenshot("screenshot.png")
                raise

            print("quiting driver")
            self.driver.quit()

    def run_driver(self):
        # Initialize driver
        self.driver = Driver(uc=True, headless2=self.option_headless)
        # Attempt to bypass
        self.bypass()

        # Initialize inner classes
        self.captcha_handler = CaptchaHandler(self.driver)
        self.eqp_manager = EnergyQuestPointsManager(self.driver, self.captcha_handler, self.auto_open_captcha)

        self.item_count = 0 # tracking the number of items found with the bot
        self.step_count = 0 # tracking the number of steps taken with the bot
        self.npc_count = 0 # tracking the number of NPC killed with the bot
        self.mat_count = 0 # tracking the number of materials looted with the bot

        # Update status before entering loop
        self.status = status_check()
        self.start_time = time.time()

        self.elapsed_time_lastcycle = 0
        self.elapsed_time = 0

        # Main loop
        while self.status == "running":
            # Update time variable
            self.elapsed_time_lastcycle = self.elapsed_time
            self.elapsed_time = get_time_elapsed_from(self.start_time)

            print_elapsed_time(self.elapsed_time)
            print()

            hour_diff = int(self.elapsed_time / 3600) - int(self.elapsed_time_lastcycle / 3600)
            if hour_diff > 0 or self.elapsed_time < 1:
                # Check for EP and QP
                print("Spending EP and QP points if maxed...")
                if self.eqp_manager.spend_points() == "stop":
                    print("Stop signal dectected, exiting main loop")
                    break

            if check_for_stop():
                break

            # Try to perform actions
            if self.loot(): self.item_count += 1
            if self.find_enemy_while_stepping(): self.npc_count += 1
            if self.item_check(): self.item_count += 1
            if self.step(): self.step_count += 1

            print(f"{self.step_count} steps taken in current session!")
            print(f"{self.item_count} items found in current session!")
            print(f"{self.npc_count} NPC killed in current session!")
            print(f"{self.item_count} materials looted in current session!")
            print()

            self.captcha_handler.delay_for_verification(time.time())

            if self.captcha_handler.exist_test('step'):
                self.captcha_handler.notify_captcha(self.auto_open_captcha)

            print("Checking status")
            self.status = status_check()
            if self.status == 'stop':
                print("Stop signal detected, exiting main loop")

def prRed(skk): print("\033[91m{}\033[00m" .format(skk))

if __name__ == '__main__':
    umiyuri = UmiyuriStepper()
    umiyuri.main()
    print("stopping script\n")