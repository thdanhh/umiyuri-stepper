import os
import string
import sys
import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from win10toast import ToastNotifier
from win11toast import toast
from functions import status_check, write_txt
import winsound
from selenium.webdriver.common.action_chains import ActionChains

def attack(driver):
    in_battle = False
    try:
        enemy = driver.find_element(By.XPATH, "//a[contains(text(), 'Attack')]")
        print("NPC found! Battle started!")
        time.sleep(1)
        open_in_new_tab(driver, enemy)
        in_battle = True
        print("Attacking...")
        attack = driver.find_element(By.XPATH, "//button[contains(text(), 'Attack')]")
        while in_battle == True:
            attack.click()
            time.sleep(0.5)

            try:
                end = driver.find_element(By.XPATH, "//a[@class='mt-2 inline-flex w-full justify-center rounded-md border border-transparent bg-gray-100 px-4 py-2 text-xs font-medium text-gray-700 shadow-sm hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 sm:text-sm']")
                hp = driver.find_element(By.XPATH, "(//div[@class='flex justify-center bg-gradient-to-r from-red-500 to-red-400 h-4 rounded-lg w-36 text-xs text-gray-100 nightwind-prevent text-center ring-1 ring-black ring-opacity-5 shadow-sm transition-all'])[2]")
                if hp.text == '':
                    end.click()
                    print("Battle ended!")
                    print()
                    in_battle = False
            except:
                pass
            try:
                exist_test(driver, 'battle')
            except:
                pass
        # Close tab
        handles = driver.window_handles
        driver.close()
        # Switch back to the old tab or window
        driver.switch_to.window(handles[0])
        time.sleep(1)
        return True
    except: 
        return False

def loot(driver):
    try:
        action = driver.find_element(By.XPATH, '//button[@class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"]')
        action.click()
        print("Material found!")
        craft = driver.find_element(By.XPATH, '//button[@id="crafting_button"]')
        print("Looting...")
        while not craft.text.strip() == "Press here to close":
            craft.click()  
            time.sleep(0.5)
        print("Material looted!")
        print()
        return True
    except:
        return False

def step(driver):
    try:
        step_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '(//button[starts-with(@id, "step_btn_")])[3]'))
        )
        if step_button.is_enabled():
            step_button.click()
            time.sleep(1)
        else:
            time.sleep(3)
            step_button.click()
        return True
    except:
        return False

def item_check(driver):
    try:
        found_item = driver.find_element(By.XPATH, "//*[text()='You have found an item!']")
        if found_item.text.strip() == "You have found an item!":
            print("You found an item!")
            rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            file_name = (f'item_{rand_str}.png')
            print(f"Item found! Don't forget to check your inventory. Screenshot saved.")
            folder_path = os.path.join(os.getcwd(), 'pages/items')
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            file_path = os.path.join(folder_path, file_name)
            driver.save_screenshot(file_path)
        return True
    except:
        return False

def exist_test(driver, captcha_type):
    captcha = ''
    if captcha_type == 'step':
        captcha = captcha = driver.find_element(By.XPATH, "(//*[text()='Press here to confirm your existence'])[2]")
    elif captcha_type == 'battle':
        captcha = driver.find_element(By.XPATH, "//*[contains(text(), 'Press here to verify')]")

    if captcha.is_displayed():
        print("Solve the captcha to continue, if you are done solving, type c then enter to continue the loop.")
        alert_sound = lambda: winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
        toaster = ToastNotifier()
        alert_sound()
        toast("Verification Detected", "Solve the captcha to continue stepping")
        with open("info.txt", 'r') as f:
            lines = f.readlines()
            try:
               status = lines[2].strip()
            except:
               status = 'stop'
        if status != 'stop':
            write_txt(3, 'captcha')
        while status_check() == "captcha" and status_check() != "stop":
            if input().lower() == "c":
                write_txt(3, "running")
                break

def delay_for_verification(start_time):
    delay = random.randint(5, 10)
    print(f"{delay} seconds delayed to avoid detection, please be patient...")
    print()
    while (time.time() - start_time < delay) and status_check() != 'stop' and status_check() != 'paused':
        time.sleep(1)

def open_in_new_tab(driver, element):
    link = element.get_attribute("href")
    driver.execute_script(f"window.open('{link}', '_blank');")
    time.sleep(1)
    # Get all windows
    handles = driver.window_handles
    # Loop through until we find a new window handle
    driver.switch_to.window(handles[1])
    time.sleep(1)
