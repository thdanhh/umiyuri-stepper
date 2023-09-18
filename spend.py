from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
from status import status_check

# UmiyuriStepper.battle()
def spend_points(self):
    print("checking current amount of points")
    self.driver.get("https://web.simple-mmo.com/user/character")

    # EP
    max_ep = self.driver.find_element(By.XPATH, '(//span[@class="text-gray-300 font-medium"])[3]').text
    max_ep_len = len(max_ep)
    max_ep = int(re.sub("[^0-9]", "", max_ep))

    current_ep = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[3]/main/div[2]/div[1]/div[9]/div[2]/div[1]/div[2]/dd/div/div[1]').text
    current_ep = int(re.sub("[^0-9]", "", current_ep[:-max_ep_len]))

    # QP
    max_qp = self.driver.find_element(By.XPATH, '(//span[@class="text-gray-300 font-medium"])[2]').text
    max_qp_len = len(max_qp)
    max_qp = int(re.sub("[^0-9]", "", max_qp))

    current_qp = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[3]/main/div[2]/div[1]/div[9]/div[1]/div[2]/div[2]/dd/div/div[1]').text
    current_qp = int(re.sub("[^0-9]", "", current_qp[:-max_qp_len]))

    ep_max = True
    qp_max = True

    if max_ep != current_ep:
        print("current EP is not maxed")
        ep_max = False
        time.sleep(0.5)
    if max_qp != current_qp:
        print("current QP is not maxed")
        qp_max = False
        time.sleep(0.5)

    if ep_max == False and qp_max == False:
        print("Returning to travel page")
        self.driver.get("https://web.simple-mmo.com/travel")
        return False 

    print("Spending points...")

    if ep_max == True:
        time.sleep(0.5)
        print("Navigating to arena")
        self.driver.get("https://web.simple-mmo.com/battle/arena")
        time.sleep(0.5)

        while current_ep > 0:
            if status_check() == 'stop':
                print("Stop signal received, exiting EP loop")
                break
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
            current_ep -= 1
            print(f'EP: {current_ep} left')
        print("EP emptied.")
        time.sleep(0.5)

    if qp_max == True:
        print("Navigating to quests page")
        time.sleep(0.5)
        self.driver.get("https://web.simple-mmo.com/quests/viewall")
        time.sleep(0.5)

        quests = self.driver.find_elements(By.CSS_SELECTOR, "li:has(.font-semibold.mr-1.text-gray-500.dark\\:text-gray-200)")
        incomplete_quest = quests[-1]
        incomplete_quest.click()
        time.sleep(0.5)

        print("Performing quests...")
        while current_qp > 0:
            if status_check() == 'stop':
                print("Stop signal received, exiting QP loop")
                break
            perform_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Perform Quest')]"))
            )
            time.sleep(1)
            perform_button.click()
            if self.captcha_handler.exist_test('quests'):
                self.captcha_handler.notify_captcha(self.auto_open_captcha)
                self.driver.refresh()
            current_qp -= 1
            print(f'QP: {current_qp} left')
        print("QP emptied")
        time.sleep(0.5)

    print("Returning to travel page")
    self.driver.get("https://web.simple-mmo.com/travel")
    return True