from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from  selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from utils import *
import random
import requests
import pyfiglet
# Define the URL of your API endpoint
from tqdm import tqdm
import time
from webdriver_manager.chrome import ChromeDriverManager

LOCAL_VERSION=1.0
# Define the total number of iterations


# Create a tqdm instance with the total number of iterations


# Simulate some task that progresses


def Bot(code_list):
    welcome_text="Hi, i'm Betbot!"
    ascii_art = pyfiglet.figlet_format(welcome_text)

    # #print ASCII art
    print(ascii_art)

    is_booting=True
    slip_limit=0
    

    # Your array


    # Choose a random element from the array
    betslip_count_limit=int(slip_limit)
    betslip_count=0
    for code in code_list:
        try:
            service=Service("chromedriver.exe")
            driver=webdriver.Chrome(service=service)

            driver.get("https://www.sportybet.com/ng/sport/football/upcoming?time=24")


            WebDriverWait(driver,60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,".m-table-row.m-content-row.match-row"))
            )

            
            match_rows = driver.find_elements(By.CSS_SELECTOR, ".m-table-row.m-content-row.match-row")
            login_form = driver.find_elements(By.CLASS_NAME, "fs-exclude")
            phone_field=login_form[0]
            password_field=login_form[1]
            phone_field.send_keys("08058876058")
            password_field.send_keys("Peaklane1")
            loginBtn = driver.find_element(By.CSS_SELECTOR, ".m-btn.m-btn-login")
            loginBtn.click()
            time.sleep(10)
            booking_code_field = driver.find_elements(By.CSS_SELECTOR, ".m-input.fs-exclude")[1]
            booking_code_field.send_keys(code)
            load_code = driver.find_elements(By.CSS_SELECTOR, ".af-button.af-button--primary")[1]
            load_code.click()
            WebDriverWait(driver,12).until(
                EC.presence_of_element_located((By.CLASS_NAME,"m-list-nav"))
            )
            bet_nav = driver.find_element(By.CLASS_NAME, "m-list-nav")
            print(bet_nav)
            # multiple=bet_nav.find_elements(By.CLASS_NAME,"m-table-cell")
            # multiple[1].click()   
            # stake_field = driver.find_element(By.CSS_SELECTOR, ".m-input.fs-exclude")
            # time.sleep(2)
            # stake_field.clear()
            # time.sleep(2)

            # stake_field.send_keys(50)
            place_bet_btn = driver.find_element(By.CSS_SELECTOR, ".af-button.af-button--primary")
            place_bet_btn.click()
            time.sleep(10)
            confirm_bet_btn = driver.find_elements(By.CSS_SELECTOR, ".af-button.af-button--primary")[1]
            confirm_bet_btn.click()
            time.sleep(7)
            driver.close()
        except Exception as e:
            print(e)
            driver.close()
            print(f"skipping code --> {code}")
    


codes=input("Please Enter you booking codes: ")
code_list=codes.split(" ")
print(code_list)
Bot(code_list)
