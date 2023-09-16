import os
import string
import sys
import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from win10toast import ToastNotifier
from win11toast import toast
from functions import write_txt
import winsound
from status import status_check
from captcha import exist_test, notify_captcha

def attack(driver, auto_open_captcha):
    in_battle = False
    try:
        enemy = driver.find_element(By.XPATH, "//a[contains(text(), 'Attack')]")
    except NoSuchElementException:
        return False
    print("NPC found! Battle started!")
    enemy.click()
    time.sleep(2)
#     open_in_new_tab(driver, enemy)
    # opening in new tab introduce some unresolved bug
    # exception: NoSuchElementException, StaleElementReferenceException

    in_battle = True
    print("Attacking...")
    attack = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//button[contains(text(), 'Attack')]"))
    )
    while in_battle == True and status_check() != 'stop':
        attack.click()
        time.sleep(0.5)

        captcha = None
        if exist_test(driver, 'battle', captcha):
            notify_captcha(captcha, auto_open_captcha)

        try:
            end = driver.find_element(By.XPATH, "//a[@class='mt-2 inline-flex w-full justify-center rounded-md border border-transparent bg-gray-100 px-4 py-2 text-xs font-medium text-gray-700 shadow-sm hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 sm:text-sm']")
            hp = driver.find_element(By.XPATH, "(//div[@class='flex justify-center bg-gradient-to-r from-red-500 to-red-400 h-4 rounded-lg w-36 text-xs text-gray-100 nightwind-prevent text-center ring-1 ring-black ring-opacity-5 shadow-sm transition-all'])[2]")
            if hp.text == '':
                end.click()
                print("Battle ended!")
                print()
                in_battle = False
        except NoSuchElementException:
            pass

        # Close tab
#         handles = driver.window_handles
#         driver.close()
#         # Switch back to the old tab or window
#         driver.switch_to.window(handles[0])
# exception: selenium.common.exceptions.InvalidSessionIdException
        time.sleep(1)
    return True

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
        craft.click()
        time.sleep(2)
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

# open new tab with link containing element specified in argument
# not in use
def open_in_new_tab(driver, element):
    link = element.get_attribute("href")
    print("before exe" + driver.current_window_handle)
    driver.execute_script(f"window.open('{link}', '_blank');")
    time.sleep(1)
    # Get all windows
    handles = driver.window_handles
    print("after exe before sw to" + driver.current_window_handle)
    # Loop through until we find a new window handle
    driver.switch_to.window(handles[1])
    print("after sw to" + driver.current_window_handle)
    time.sleep(1)
