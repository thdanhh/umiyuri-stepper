from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
from status import status_check, check_for_stop
from action import attack as _attack

class EnergyQuestPointsManager:
    attack = _attack

    def __init__(self, driver, captcha_handler):
        self.driver = driver
        self.captcha_handler = captcha_handler
        self.current_ep = 0
        self.current_qp = 0

    def spend_points(self):
        print("Spending EP and QP points if maxed...")
        ep_is_maxed, qp_is_maxed = self.check_for_maxed_points()

        if check_for_stop():
            return "stop"

        if not ep_is_maxed and not qp_is_maxed:
            print("EP and QP is not maxed, continuing to step\n")
            return "continue"

        if ep_is_maxed:
            if not self.spend_ep():
                return "stop"

        if qp_is_maxed:
            if not self.spend_qp():
                return "stop"

        print("Returning to travel page")
        self.driver.get("https://web.simple-mmo.com/travel?new_page=true")
        return "continue"

    def check_for_maxed_points(self):
        user_menu = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/nav/div/div/div[2]/div[3]/div[1]/button[2]')
        user_menu.click()
        time.sleep(1)
        return self.check_for_maxed_ep(), self.check_for_maxed_qp()

    def check_for_maxed_ep(self):
        max_ep = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/nav/div/div/div[2]/div[3]/div[2]/div/div[3]/div/div/span[2]/div[2]/div[2]/div[2]/p/span[2]/span').text
        # max_ep_len = len(max_ep)
        max_ep = int(max_ep)

        current_ep = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/nav/div/div/div[2]/div[3]/div[2]/div/div[3]/div/div/span[2]/div[2]/div[2]/div[2]/p/span[1]').text
        self.current_ep = int(current_ep)

        if max_ep != self.current_ep:
            ep_max = False
            time.sleep(0.5)
            return False
        else:
            return True

    def check_for_maxed_qp(self):
        max_qp = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/nav/div/div/div[2]/div[3]/div[2]/div/div[3]/div/div/span[3]/div[2]/div[2]/div[2]/p/span[2]/span').text
        max_qp = int(max_qp)

        current_qp = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/nav/div/div/div[2]/div[3]/div[2]/div/div[3]/div/div/span[3]/div[2]/div[2]/div[2]/p/span[1]').text
        self.current_qp = int(current_qp)

        if max_qp != self.current_qp:
            qp_max = False
            time.sleep(0.5)
            return False
        else:
            return True

    def spend_ep(self):
        print("Spending EP")
        time.sleep(0.25)
        print("Navigating to arena")
        self.driver.get("https://web.simple-mmo.com/battle/arena")
        time.sleep(0.5)

        while self.current_ep > 0:
            if status_check() == 'stop':
                print("Stop signal received, exiting EP loop")
                return False
            print("Generating enemy")
            generate_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '(//button[@class="inline-flex items-center rounded-md border border-gray-300 bg-white px-3 py-2 text-sm font-medium leading-4 text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"])[1]'))
            )
            generate_button.click()
            time.sleep(0.5)
            generate_blue = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '(//button[@class="nightwind-prevent inline-flex w-full justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-xs sm:text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"])[1]'))
            )
            generate_blue.click()
            time.sleep(0.5)
            battle_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '(//button[@class="nightwind-prevent inline-flex w-full justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-xs sm:text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"])[2]'))
            )
            battle_button.click()
            self.attack()
            self.current_ep -= 1
            print(f'EP: {self.current_ep} left')
        print("EP emptied.")
        time.sleep(0.5)
        return True

    def spend_qp(self):
        print("Spending QP")
        time.sleep(0.25)
        print("Navigating to quests page")
        self.driver.get("https://web.simple-mmo.com/quests/viewall")
        time.sleep(0.5)

        quests = self.driver.find_elements(By.CSS_SELECTOR, "li:has(.font-semibold.mr-1.text-gray-500.dark\\:text-gray-200)")
        incomplete_quest = quests[-1]
        incomplete_quest.click()
        time.sleep(0.5)

        print("Performing quests...")
        while self.current_qp > 0:
            if status_check() == 'stop':
                print("Stop signal received, exiting QP loop")
                return False
            perform_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Perform Quest')]"))
            )
            time.sleep(1)
            perform_button.click()
            if self.captcha_handler.exist_test('quests'):
                self.captcha_handler.notify_captcha()
                self.driver.refresh()
            self.current_qp -= 1
            print(f'QP: {self.current_qp} left')
        print("QP emptied")
        time.sleep(0.5)
        return True