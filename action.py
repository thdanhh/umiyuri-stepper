import os
import string
import sys
import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from functions import write_txt
import winsound
from status import status_check

# Umiyuri.find_enemy
def find_enemy_while_stepping(self):
    try:
        enemy = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Attack')]")
    except NoSuchElementException:
        return False
    print("NPC found! Battle started!")
    enemy.click()
    time.sleep(2)
    self.attack()
    return True

# UmiyuriStepper.attack()
def attack(self):
    print("Entering battle")
    in_battle = True

    # Find attack button
    attack = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Attack')]"))
    )
    while in_battle == True:
        # Check for script stop signal
        if status_check() == 'stop':
            print("Stop signal received, exiting attack loop")
            break

        # Click the attack button
        print("Attacking...")
        attack.click()

        attack = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Attack')]"))
        )

        # Enemy's hp
        hp = self.driver.find_element(By.XPATH, "(//div[@class='flex justify-center bg-gradient-to-r from-red-500 to-red-400 h-4 rounded-lg w-36 text-xs text-gray-100 nightwind-prevent text-center ring-1 ring-black ring-opacity-5 shadow-sm transition-all'])[2]")

        if hp.text != '':
            print(f"Enemy hp: {hp.text}")

        if hp.text == '':
            print("Enemy killed")
            # Check for captcha
            if self.captcha_handler.exist_test('battle'):
                self.captcha_handler.notify_captcha()
                self.driver.get("https://web.simple-mmo.com/travel")
                return True

            # End battle
            end = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//a[@class='mt-2 inline-flex w-full justify-center rounded-md border border-transparent bg-gray-100 px-4 py-2 text-xs font-medium text-gray-700 shadow-sm hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 sm:text-sm']"))
            )
            end.click()
            print("Battle ended!")
            print()
            in_battle = False
        # Check for captcha
        if self.captcha_handler.exist_test('battle'):
            self.captcha_handler.notify_captcha()
    return True

# UmiyuriStepper.loot()
def loot(self):
    try:
        skill_issue = self.driver.find_element(By.XPATH, '//*[contains(text(), "Your skill level isn\'t high enough to do this. You need to have a")]')
        return False
    except:
        pass
    try:
        gather = self.driver.find_element(By.XPATH, '//button[@class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"]')
    except:
        return False
    gather.click()

    print("Material found!")
    craft = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@id="crafting_button"]'))
    )

    print("Looting...")
    while not craft.text.strip() == "Press here to close":
        craft.click()
        craft = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@id="crafting_button"]'))
        )
    print("Material looted!")
    print()
    craft.click()
    time.sleep(2)
    return True

# UmiyuriStepper.step()
def step(self):
    MAX_STEP_DELAY = 20 # Estimated
    try:
        step_button = WebDriverWait(self.driver, MAX_STEP_DELAY).until(
            EC.element_to_be_clickable((By.XPATH, '(//button[starts-with(@id, "step_btn_")])[3]'))
        )
    except TimeoutException:
        self.driver.refresh()
        return False
    print("Stepping...")
    print()
    step_button.click()
    return True

# UmiyuriStepper.item_check()
def item_check(self):
    try:
        found_item = self.driver.find_element(By.XPATH, "//*[text()='You have found an item!']")
    except NoSuchElementException:
        return False

    print(f"Item found! Don't forget to check your inventory. Screenshot saved.")
    rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    file_name = (f'item_{rand_str}.png')
    folder_path = os.path.join(os.getcwd(), 'pages/items')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, file_name)
    self.driver.save_screenshot(file_path)
    return True

# UmiyuriStepper.open_in_new_tab()
# open new tab with link containing element specified in argument
# not in use
def open_in_new_tab(self, element):
    link = element.get_attribute("href")
    print("before exe" + self.driver.current_window_handle)
    self.driver.execute_script(f"window.open('{link}', '_blank');")
    time.sleep(1)
    # Get all windows
    handles = self.driver.window_handles
    print("after exe before sw to" + self.driver.current_window_handle)
    # Loop through until we find a new window handle
    self.driver.switch_to.window(handles[1])
    print("after sw to" + self.driver.current_window_handle)
    time.sleep(1)
