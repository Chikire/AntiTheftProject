# testing the dht sensor with firebase

import time
import board
import adafruit_dht
import pyrebase
# from gpiozero import DigitalInputDevice
import RPi.GPIO as GPIO

# set up the gpio mode
GPIO.setmode(GPIO.BCM)

config = {
  "apiKey": "AIzaSyBjSuZOOPocpbur-XeybMrXpc48u4hLxlU",
  "authDomain": "anti-theft-system-afa8a.firebaseapp.com",
  "databaseURL": "https://anti-theft-system-afa8a-default-rtdb.firebaseio.com/",
  "storageBucket": "anti-theft-system-afa8a.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()



# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D6)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
dhtDevice = adafruit_dht.DHT11(board.D6, use_pulseio=False)

while True:
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        
        
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
            temperature_f, temperature_c, humidity
            )
    
        )
        
        data = {
        "Temperature" : temperature_c,
        "Humidity" : humidity
        }
        db.child("Status").push(data)

        db.update(data)
        print("Sent to Firebase")

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
    #finally:
     #   GPIO.cleanup()
    time.sleep(2.0)
    
