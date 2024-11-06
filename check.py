import requests
import time
import mysql.connector
from configparser import ConfigParser
from dotenv import load_dotenv
import os
load_dotenv()
config=ConfigParser()
config.read("db_config.ini")

LOCATIONIQ_API_KEY2 = os.getenv("LOCATIONIQ_API_KEY2")
def connect_to_db():
    db_config={
        "host":config["mysql"]["host"],
        "user":config["mysql"]["user"],
        "password":config["mysql"]["password"],
        "database":config["mysql"]["database"]
    }
    mydb = mysql.connector.connect(**db_config)
    return mydb

def update_confimed_city_name(db,mycursor,id,lat,lon):
    url=f"https://us1.locationiq.com/v1/reverse.php?key={LOCATIONIQ_API_KEY2}&lat={lat}&lon={lon}&format=json"
    response=requests.get(url)
    data=response.json()
    try:
        confirmed_city_name=data["address"]["city"]
    except:
        confirmed_city_name=""
    sql = "UPDATE `main_geo_city_incorporated_raza` SET confirmed_city_name = %s WHERE id = %s"
    val = (confirmed_city_name, id)
    mycursor.execute(sql, val)
    db.commit()
    print(f"Updated {id} with {confirmed_city_name}")

if __name__ == '__main__':
    db = connect_to_db()
    mycursor = db.cursor()
    mycursor.execute("SELECT * FROM `main_geo_city_incorporated_raza`")
    data = mycursor.fetchall()
    for i in range(6000,10000):
        id=data[i][0]
        lat=data[i][3]
        lon=data[i][2]
        confirmed_city_name=data[i][4]
        if confirmed_city_name=="":
            update_confimed_city_name(db,mycursor,id,lat,lon)
        time.sleep(1)
        