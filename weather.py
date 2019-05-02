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

url = 'http://192.168.1.14:8000/api/weather/eMGzj8KOyITdwgnJA1Gd'

count = 0

while True: 
    result = instance.read() 
    if result.is_valid(): 
        if count >= 1: # Only read the saesor data after the first reading
            temperature = bmp280.get_temperature()
            pressure = bmp280.get_pressure()
            temp_fahrenheit = ((temperature * 9/5) + 35)
            now = datetime.datetime.now()
            print("Humidity %d %%" % result.humidity)
            print("Pressure {:05.2f}hPa".format(pressure))
            print("Temp {:05.2f}*F".format(temp_fahrenheit))
            print(now.strftime("%Y-%m-%d %H:%M:%S"))
            payload = {"temp": temp_fahrenheit, "humidity": result.humidity, "pressure": pressure, "event_time": str(now)}
        else: # Read the data for the first time and null it out. Most of the sensor data on the first pass is bad data
            temperature = bmp280.get_temperature()
            pressure = bmp280.get_pressure()
            payload = {"temp": "null", "humidity": "null", "pressure": "null", "event_time": str(now)}
        r = requests.post(url, json=payload)
        count = count + 1
        time.sleep(1)


GPIO.cleanup()
