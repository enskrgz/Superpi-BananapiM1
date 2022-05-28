#raspberrypi code
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
            perc = mq.MQPercentage()
            #test 
            #sys.stdout.write("\r")
            #sys.stdout.write("\033[K")
            #sys.stdout.write("LPG: %g ppm, CO: %g ppm, Smoke: %g ppm" % (perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))
            #sys.stdout.flush()
            gasvalue =perc["GAS_LPG"]
            covalue = perc["CO"]
            smokevalue = perc["SMOKE"]
            time.sleep(0.1)
            result = instance.read()
            if result.is_valid():
                #test çıktıları
                #print("Last valid input: " + str(datetime.datetime.now()))
                #print("Temperature: %-3.1f C" % result.temperature)
                #print("Humidity: %-3.1f %%" % result.humidity)
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
