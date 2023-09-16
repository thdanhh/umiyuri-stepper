from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
from status import status_check

def quests(self):
    print("checking current amount of QP points")
    self.driver.get("https://web.simple-mmo.com/user/character")

    max_qp = self.driver.find_element(By.XPATH, '(//span[@class="text-gray-300 font-medium"])[2]').text
    max_qp_len = len(max_qp)
    max_qp = int(re.sub("[^0-9]", "", max_qp))

    current_qp = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div[3]/main/div[2]/div[1]/div[9]/div[1]/div[2]/div[2]/dd/div/div[1]').text
    current_qp = int(re.sub("[^0-9]", "", current_qp[:-max_qp_len]))

    if max_qp != current_qp:
        print("current QP is not maxed, returning")
        self.driver.get("https://web.simple-mmo.com/travel")
        return False

    print("Navigating to quests page")
    time.sleep(0.5)
    self.driver.get("https://web.simple-mmo.com/quests/viewall")
    time.sleep(0.5)

    quests = self.driver.find_elements(By.CSS_SELECTOR, "li:has(.font-semibold.mr-1.text-gray-500.dark\\:text-gray-200)")
    incomplete_quest = quests[-1]
    incomplete_quest.click()
    time.sleep(0.5)

    print("Performing quests")
    while current_qp > 0:
        if status_check() == 'stop':
            print("Stop signal received, exiting QP loop")
            break
        perform_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Perform Quest')]"))
        )
        perform_button.click()
        if self.captcha_handler.exist_test('quests'):
            self.captcha_handler.notify_captcha(self.auto_open_captcha)
        current_qp -= 1
    print("QP emptied, returning to travel page")
    self.driver.get("https://web.simple-mmo.com/travel")
    return True