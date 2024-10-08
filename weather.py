import time
import json
import dht11
import datetime
import requests
import RPi.GPIO as GPIO
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bmp280 import BMP280



print('/////////////////////////////') 
print('//Derek\'s Weather Station///') 
print('/////////////////////////////')  
print('/////////////   /////////////') 
print('////////////   //////////////') 
print('///////////   ///////////////') 
print('//////////      /////////////') 
print('////////////   //////////////') 
print('///////////   ///////////////') 
print('//////////   ////////////////') 
print('///////////   ///////////////') 
print('//////////  /////////////////') 
print('///////// ///////////////////') 
print('/////////////////////////////')


GPIO.setmode(GPIO.BCM)
GPIO.cleanup()



bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)


instance = dht11.DHT11(pin=14)

def get_seonsor_data():
    temperature = bmp280.get_temperature()
    pressure = bmp280.get_pressure()
    temp_fahrenheit = ((temperature * 9/5) + 35)
    now = datetime.datetime.utcnow()
    # result = instance.read()
    # if result.is_valid():
    #     humidity = result.humidity
    # else:
    #     humidity = ""
    humidity = 50

    if not (humidity and pressure and temp_fahrenheit): #Check if any of the values have not been set and try again
        print('-- BAD DATA SLEEPING --')
        time.sleep(0.01)
        return get_seonsor_data()
    else: #Print out the data and return it in json
        print("Humidity %d %%" % humidity)
        print("Pressure {:05.2f}hPa".format(pressure))
        print("Temp {:05.2f}*F".format(temp_fahrenheit))
        print(now.strftime("%Y-%m-%d %H:%M:%S"))
        payload = {"temp": temp_fahrenheit, "humidity": humidity, "pressure": pressure, "event_time": str(now)}
        print("Request payload:")
        print(payload)
        return payload



url = 'https://api.derkweather.com/api/weather/eMGzj8KOyITdwgnJA1Gd'
count = 0

while True: 
    if count >= 1:
        # Only read the saesor data after the first reading
        data = get_seonsor_data()
        print("Data:")
        print(data)
    else: 
        # Read the data for the first time and null it out. Most of the sensor data on the first pass is bad data
        get_seonsor_data()
        data = ""
        
    if data:
        print("About to send request")
        r = requests.post(url, json=data)
        print("Response status code:")
        print(r.status_code)
    count = count + 1
    time.sleep(15)


GPIO.cleanup()
