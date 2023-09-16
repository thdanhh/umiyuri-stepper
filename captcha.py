import time
import random
import os
import winsound
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from win10toast import ToastNotifier
from win11toast import toast
from status import status_check, write_status_to_txt, read_status_from_txt

def delay_for_verification(start_time):
    delay = random.randint(5, 10)
    print(f"{delay} seconds delayed to avoid detection, please be patient...")
    print()
    while (time.time() - start_time < delay) and status_check() != 'stop' and status_check() != 'paused':
        time.sleep(1)

def exist_test(driver, captcha_type, captcha):
    try:
        if captcha_type == 'step':
            captcha = driver.find_element(By.XPATH, "(//*[text()='Press here to confirm your existence'])[2]")
        elif captcha_type == 'battle':
            captcha = driver.find_element(By.XPATH, "//*[contains(text(), 'Press here to verify')]")
        return captcha.is_displayed()
    except NoSuchElementException:
        return False

def notify_captcha(captcha, auto_open_captcha):
    # Automatically open verify page on browser
    if auto_open_captcha:
        os.system("start \"\" https://web.simple-mmo.com/i-am-not-a-bot?new_page=true")

    print("Captcha found")
    print("Solve the captcha to continue, if you are done solving, type c then enter to continue the loop.")
    print("https://web.simple-mmo.com/i-am-not-a-bot")
    alert_sound = lambda: winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
    toaster = ToastNotifier()
    alert_sound()
    toast("Verification Detected", "Solve the captcha to continue stepping")

    status = read_status_from_txt()
    if status == 'stop':
        return

    write_status_to_txt("captcha")
    while read_status_from_txt() == "captcha":
        if input().lower() == 'c':
            if read_status_from_txt() == 'stop':
                return
            write_status_to_txt("running")
            return
