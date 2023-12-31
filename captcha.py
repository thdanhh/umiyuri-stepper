import time
import random
import os
import winsound
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from status import status_check, write_status_to_txt, read_status_from_txt

class CaptchaHandler:
    def __init__(self, driver, auto_open_captcha):
        self.driver = driver
        self.auto_open_captcha = auto_open_captcha

    def delay_for_verification(self, start_time):
        delay = random.randint(5, 10)
        print(f"{delay} seconds delayed to avoid detection, please be patient...")
        print()
        while (time.time() - start_time < delay):
            status = status_check()
            if status == 'stop' or status == 'paused':
                break
            time.sleep(1)

    def exist_test(self, captcha_type):
        print("Checking for verification...\n")
        try:
            if captcha_type == 'step':
                self.captcha = self.driver.find_element(By.XPATH, "(//*[text()='Press here to confirm your existence'])[2]")
            elif captcha_type == 'battle' or 'quests':
                self.captcha = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Press here to verify')]")
            return self.captcha.is_displayed()
        except NoSuchElementException or StaleElementReferenceException:
            return False

    def notify_captcha(self, link):
        # Automatically open verify page on browser
        if self.auto_open_captcha:
            os.system("start \"\" https://web.simple-mmo.com/i-am-not-a-bot?new_page=true")

        print("Captcha found, solve the captcha to continue.")
        print("https://web.simple-mmo.com/i-am-not-a-bot?new_page=true")
        self.driver.get("https://web.simple-mmo.com/i-am-not-a-bot?new_page=true")

        alert_sound = lambda: winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
        alert_sound()

        status = read_status_from_txt()
        if status == 'stop':
            return

        write_status_to_txt("captcha")
        status = "captcha"
        captcha_solved = False
        while status == 'captcha': 
            try:
                time.sleep(1)
                self.driver.refresh()
                verified_text = self.driver.find_element(By.XPATH, '//*[contains(text(), "You have passed.")]')
                captcha_solved = True
            except NoSuchElementException:
                pass
            if captcha_solved:
                print("Captcha solved, continuing...")
                print()
                status = read_status_from_txt()
                if status == 'stop' or status == 'paused':
                    return
                write_status_to_txt("running")
                self.driver.get(link)
                return
