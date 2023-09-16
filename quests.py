from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time

def quests(self):
    try:
        self.driver.get("https://web.simple-mmo.com/user/character")
        max_qp = self.driver.find_element(By.XPATH, '(//span[@class="text-gray-300 font-medium"])[2]').text
        max_qp = int(re.sub("[^0-9]", "", max_qp))
        current_qp = self.driver.find_element(By.XPATH, f'//div[contains(text(), {max_qp})]').text
        current_qp = int(re.sub("[^0-9]", "", current_qp[2:]))
    except:
        self.driver.get("https://web.simple-mmo.com/travel")
        return False
    time.sleep(0.5)
    self.driver.get("https://web.simple-mmo.com/quests/viewall")
    time.sleep(0.5)
    quests = self.driver.find_elements(By.CSS_SELECTOR, "li:has(.font-semibold.mr-1.text-gray-500.dark\\:text-gray-200)")
    incomplete_quest = quests[-1]
    incomplete_quest.click()
    time.sleep(0.5)
    while current_qp > 0 and status_check() != 'stop':
        perform_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Perform Quest')]"))
        )
        perform_button.click()
        if self.captcha_handler.exist_test('quests'):
            self.captcha_handler.notify_captcha(self.auto_open_captcha)
        current_qp -= 1
        self.driver.get("https://web.simple-mmo.com/travel")