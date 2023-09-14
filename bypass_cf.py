import time
import os
import win10toast
import win11toast
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from win10toast import ToastNotifier
from win11toast import toast

def bypass(driver):
    with open("info.txt") as f:
        lines = f.readlines()
        email = lines[0].strip()
        password = lines[1].strip()
    # Bypass cloudflare and login
    driver.execute_script('window.open("https://web.simple-mmo.com/login", "_blank");')
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[-1])

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
    # Wait for the login button to be clickable
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    # Click the login button
    login_button.click()

    # Wait for the page to load
    time.sleep(3)

    # Navigate to the travel page
    driver.get("https://web.simple-mmo.com/travel")

    print("Welcome to Umiyuri Stepper!")
    toast('Welcome to Umiyuri Stepper!')

    # Wait for the page to load
    time.sleep(3)

    alert_sound = lambda: winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
    toaster = ToastNotifier()