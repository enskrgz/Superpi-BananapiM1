#BANANA PI İLE ORTAM HAVA KALİTE İZLEME SİSTEMİ
# Ana Kod Sayfası 
from mq import *
import sys
import asyncio
import socketio
import RPi.GPIO as GPIO
import dht11
import time
import datetime

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)  #kartı üzerindeki pinlerin bilgisini alma


instance = dht11.DHT11(pin=18) # DHT11 sensör verisini pin18 den alıyoruz.
try:
  mq = MQ();
        while True:
            perc = mq.MQPercentage()    #mq kütüphanesinin içerisindeki MQPercentage() fonksiyonu incelenerek oluşturulmuştur.
            gasvalue =perc["GAS_LPG"]
            covalue = perc["CO"]
            smokevalue = perc["SMOKE"]
            time.sleep(0.1)
            result = instance.read()     #dht11 kütüphanesi içerisinde instance fonksiyonu incelenerek oluşturulmuştur.
            if result.is_valid():
                datetimevalue = str(datetime.datetime.now())
                tempvalue = result.temperature
                humidityvalue = result.humidity

            time.sleep(6)
            
except KeyboardInterrupt:    
    print("Cleanup")
    GPIO.cleanup()


sio = socketio.AsyncClient()

@sio.event
async def connect():
    print('connection established')

@sio.event
async def message(data):
    data = {
      "LPG:": gasvalue,
      "CO²": covalue,
      "SMOKE": smokevalue,
      "DATETIME": datetimevalue,
      "TEMPERATURE": tempvalue,
      "HUMIDITY": humidityvalue
    }
    print('message received with ', data)
    await sio.emit('fromAPI', {'msgFromPy': 'my response'})

@sio.event
async def disconnect():
    print('disconnected from server')

async def main():
    await sio.connect('http://localhost:5000')
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(main())
