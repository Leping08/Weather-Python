import time
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

while True: 
    result = instance.read() 
    if result.is_valid(): 
        temperature = bmp280.get_temperature()
        pressure = bmp280.get_pressure()
        print("Humidity %d %%" % result.humidity)
        print("Pressure {:05.2f}hPa".format(pressure))
        print("Temp {:05.2f}*F".format((temperature * 9/5) + 35))
        time.sleep(1)


GPIO.cleanup()
