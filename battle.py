from selenium.webdriver.common.by import By
import re
import time

# UmiyuriStepper.battle()
def battle(self):
    try:
        self.driver.get("https://web.simple-mmo.com/user/character")
        max_ep = self.driver.find_element(By.XPATH, '(//span[@class="text-gray-300 font-medium"])[3]').text
        max_ep = int(re.sub("[^0-9]", "", max_ep))
        current_ep = self.driver.find_element(By.XPATH, f'//div[contains(text(), {max_ep})]').text
        current_ep = int(re.sub("[^0-9]", "", current_ep[2:]))
    except:
        self.driver.get("https://web.simple-mmo.com/travel")
        return False
    time.sleep(0.5)
    self.driver.get("https://web.simple-mmo.com/battle/arena")
    time.sleep(0.5)
    while current_ep > 0 and status_check() != 'stop':
        generate_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '(//button[@class="inline-flex items-center rounded-md border border-gray-300 bg-white px-3 py-2 text-sm font-medium leading-4 text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"])[1]'))
        )
        generate_button.click()
        generate_blue = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '(//button[@class="nightwind-prevent inline-flex w-full justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-xs sm:text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"])[1]'))
        )
        generate_blue.click()
        battle_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '(//button[@class="nightwind-prevent inline-flex w-full justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-xs sm:text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"])[2]'))
        )
        battle_button.click()
        self.attack()
        current_ep -= 1
    self.driver.get("https://web.simple-mmo.com/travel")
    return True