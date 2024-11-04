import mysql.connector
import pandas as pd
import requests
import dotenv
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import threading
from configparser import ConfigParser

dotenv.load_dotenv()
config=ConfigParser()
config.read("db_config.ini")

LOCATIONIQ_API_KEY = os.getenv("LOCATIONIQ_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_EMBED_API_KEY")


def connect_to_db():
    db_config={
        "host":config["mysql"]["host"],
        "user":config["mysql"]["user"],
        "password":config["mysql"]["password"],
        "database":config["mysql"]["database"]
    }
    mydb = mysql.connector.connect(**db_config)
    return mydb

def read_data_from_db(db):
    mycursor = db.cursor()
    mycursor.execute("SELECT * FROM `main_geo_city_incorporated_raza`")
    data = mycursor.fetchall()
    return data,mycursor

def get_driver():
    options=Options()
    options.add_argument("--start-maximized")
    options.add_argument("no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36')

    chrome_install=ChromeDriverManager().install()
    folder_path = os.path.dirname(chrome_install)
    chromedriver_path = os.path.join(folder_path, 'chromedriver.exe')
    service = ChromeService(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def scrape_embed_maps(driver,lat,lon):
    driver.get(f"https://www.google.com/maps/place//@{lat},{lon},17z")
    time.sleep(1)
    share_button = driver.find_element(By.XPATH, "//button[@aria-label='Share ']")
    share_button.click()
    time.sleep(1)
    embed_button = driver.find_element(By.XPATH, "//button[.='Embed a map']")
    embed_button.click()
    time.sleep(1)
    input_box=driver.find_element(By.XPATH, "//input[@jsaction='pane.embedMap.clickInput']")
    embed_code=input_box.get_attribute("value")
    return embed_code

def get_locationiq_data(lat,lon):
    url = f"https://us1.locationiq.com/v1/reverse?key={LOCATIONIQ_API_KEY}&lat={lat}&lon={lon}&format=json"
    response = requests.get(url)
    response_data = response.json()
    try:
        city_name = response_data["address"]["city"]
    except:
        city_name = ""
    try:
        county_name = response_data["address"]["county"]
    except:
        county_name = ""
    try:
        state_name = response_data["address"]["state"]
    except:
        state_name = ""
    return city_name,county_name,state_name


def update_db(db,city,lat,lon,confirmed_city_name,county_name,state_name,embed_code):
    mycursor = db.cursor()
    sql="UPDATE `main_geo_city_incorporated_raza` SET `confirmed_city_name`=%s,`county_name`=%s,`state_name`=%s,`google_maps_embed_code`=%s WHERE `name`=%s and `lat`=%s and `lon`=%s"
    val = (confirmed_city_name,county_name,state_name,embed_code,city,lat,lon)
    mycursor.execute(sql, val)
    db.commit()

    
        
if __name__ == "__main__":
    db=connect_to_db()
    db_data,cursor_retrieve = read_data_from_db(db)
    driver=get_driver()
    for i in range(10,len(db_data)):
        city_name = db_data[i][1]  
        lon = db_data[i][2]        
        lat = db_data[i][3]
        embed_code = scrape_embed_maps(driver,lat,lon)
        confirmed_city_name,county_name,state_name = get_locationiq_data(lat,lon)
        update_db(db,city_name,lat,lon,confirmed_city_name,county_name,state_name,embed_code)
        print(f"Updated row {i+1}")

    
    


