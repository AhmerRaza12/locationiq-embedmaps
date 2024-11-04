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

dotenv.load_dotenv()

LOCATIONIQ_API_KEY = os.getenv("LOCATIONIQ_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_EMBED_API_KEY")

def read_data_from_db():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="p13621_kammaikii"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM `main_geo_city_incorporated_raza`")
    data = mycursor.fetchall()
    return data,mycursor


    



db_data,cursor_retrieve = read_data_from_db()   
print(cursor_retrieve.rowcount)

# for i in range(2):
    
#     city_name = data[i][1]  
#     lon = data[i][2]        
#     lat = data[i][3]
#     print(city_name, lon, lat)
#     embed_url = f"https://www.google.com/maps/embed/v1/place?key={GOOGLE_MAPS_API_KEY}&q={lat},{lon}"
#     iframe_code=f"""
#     <iframe
#       width="600"
#       height="450"
#       frameborder="0" 
#       style="border:0"
#       src="{embed_url}" 
#       allowfullscreen>
#     </iframe>
#     """

#     print(iframe_code)
#     url = f"https://us1.locationiq.com/v1/reverse?key={locationiq_api_key}&lat={lat}&lon={lon}&format=json"
#     response = requests.get(url)
#     response_data = response.json()
#     try:
#         city_name = response_data["address"]["city"]
#     except:
#         city_name = ""
#     try:
#         county_name = response_data["address"]["county"]
#     except:
#         county_name = ""
#     try:
#         state_name = response_data["address"]["state"]
#     except:
#         state_name = ""
#     print(city_name, county_name, state_name)
        
        

    


