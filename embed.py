import mysql.connector
import pandas as pd
import requests
import dotenv
import os


dotenv.load_dotenv()

locationiq_api_key = os.getenv("LOCATIONIQ_API_KEY")
# Connect to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="p13621_kammaikii"
)

API_KEY="AIzaSyDy5rHSzj1qoFEwi09Im7ycOMTAEf-kaUQ"

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM `main_geo_city_incorporated_raza`")
data = mycursor.fetchall()
# print the column names
print(mycursor.column_names)
for i in range(2):
    
    city_name = data[i][1]  
    lon = data[i][2]        
    lat = data[i][3]
    print(city_name, lon, lat)
    # based on the latitude and longitude, we can generate the embed url, we have lat and lon at index 2 and 3
    embed_url = f"https://www.google.com/maps/embed/v1/place?key={API_KEY}&q={lat},{lon}"
    iframe_code=f"""
    <iframe
      width="600"
      height="450"
      frameborder="0" 
      style="border:0"
      src="{embed_url}" 
      allowfullscreen>
    </iframe>
    """

    print(iframe_code)
    # make a request to the locationiq api to get the city name https://us1.locationiq.com/v1/reverse?key=, &lat=, &lon=, &format=json
    url = f"https://us1.locationiq.com/v1/reverse?key={locationiq_api_key}&lat={lat}&lon={lon}&format=json"
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
    print(city_name, county_name, state_name)
        
        

    


