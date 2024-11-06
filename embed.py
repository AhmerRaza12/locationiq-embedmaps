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


def scrape_embed_maps(driver,lat,lon,name,confirmed_city_name,county_name,state_name):
    try:
        driver.get(f"https://www.google.com/maps/place/{name},{county_name},{state_name}/,17z")
        time.sleep(1)
        share_button=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-value='Share']")))
        share_button.click()
        embed_button=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[.='Embed a map']")))
        driver.execute_script("arguments[0].click();", embed_button)
        input_box=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@jsaction='pane.embedMap.clickInput']")))
        input_box=driver.find_element(By.XPATH, "//input[@jsaction='pane.embedMap.clickInput']")
        try:
            embed_code=input_box.get_attribute("value")
        except:
            embed_code=""
    except Exception as e:
        print(f"Error occured in extracting embed code for {name},{county_name},{state_name} with error {e}")
        embed_code=""
        pass
        
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
    for i in range(1720,len(db_data)):
        city_name = db_data[i][1]  
        lon = db_data[i][2]        
        lat = db_data[i][3]
        confirmed_city_name,county_name,state_name = get_locationiq_data(lat,lon)
        embed_code = scrape_embed_maps(driver,lat,lon,name=city_name,confirmed_city_name=confirmed_city_name,state_name=state_name,county_name=county_name)
        update_db(db,city_name,lat,lon,confirmed_city_name,county_name,state_name,embed_code)

    
    


