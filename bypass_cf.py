import time
import os
import win10toast
import win11toast
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from win10toast import ToastNotifier
from win11toast import toast
from functions import read_txt
from status import status_check

def bypass(driver):
    if status_check() == 'stop':
        return

    email = read_txt("info.txt", 1)
    password = read_txt("info.txt", 2)

    print("opening login page")
    driver.get("https://web.simple-mmo.com/login")
    print("waiting to bypass")
    time.sleep(4)

    try:
        # Wait for the email field to be visible
        email_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "email"))
        )
        # Enter the user's email from file or user input
        email_field.send_keys(email)
        # Wait for the password field to be visible
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "password"))
        )
        # Enter the user's password from file or user input
        password_field.send_keys(password)
    except TimeoutException:
        raise TimeoutException

    # Wait for the login button to be clickable
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    # Click the login button
    login_button.click()
    print("login successfully")

    # Navigate to the travel page
    print("navigating to travel page")
    driver.get("https://web.simple-mmo.com/travel")

    print("Welcome to Umiyuri Stepper!")
    toast('Welcome to Umiyuri Stepper!')

    alert_sound = lambda: winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
    toaster = ToastNotifier()