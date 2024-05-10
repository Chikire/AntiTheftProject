# 2024 KELVIN OBIOHA

import mpu6050
import time
import board
import adafruit_dht
import pyrebase
# from gpiozero import DigitalInputDevice
import RPi.GPIO as GPIO



# set up the gpio mode
GPIO.setmode(GPIO.BCM)
mpu6050 = mpu6050.mpu6050(0x68)

config = {
  "apiKey": "AIzaSyBjSuZOOPocpbur-XeybMrXpc48u4hLxlU",
  "authDomain": "anti-theft-system-afa8a.firebaseapp.com",
  "databaseURL": "https://anti-theft-system-afa8a-default-rtdb.firebaseio.com/",
  "storageBucket": "anti-theft-system-afa8a.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

#set up the pin for reading the dO output
DO_PIN = 18
IRPin = 17

GPIO.setup(IRPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setup(DO_PIN, GPIO.IN)

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D5)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
dhtDevice = adafruit_dht.DHT11(board.D5, use_pulseio=False)
# Define a function to read the sensor data
def read_sensor_data():
    # Read the accelerometer values
    accelerometer_data = mpu6050.get_accel_data()

    # Read the gyroscope values
    gyroscope_data = mpu6050.get_gyro_data()

    # Read temp
    temperature = mpu6050.get_temp()

    return accelerometer_data, gyroscope_data, temperature

def capture_image():
    camera_config = piCam.create_preview_configuration()
    piCam.configure(camera_config)
    piCam.start_preview(Preview.QTGL)
    piCam.start()
    time.sleep(1)
    piCam.capture_file('/home/nextech/alert.jpg')
    time.sleep(2)
    piCam.stop_preview()
    print('Image Captured successfully')
    time.sleep(1)
    
while True:
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        gas_present = GPIO.input(DO_PIN)
        # Read the sensor data
        accelerometer_data, gyroscope_data, temperature = read_sensor_data()
        #motion_state = GPIO.input(MOTION_PIN)
        IR_state = GPIO.input(IRPin)
        
        if IR_state == GPIO.LOW:
            ir_state = "MOTION DETECTED"
            capture_image()
        else:
            ir_state = "NO MOTION"
            piCam.stop()
        
        if gas_present == GPIO.LOW:
            gas_state = "Gas Present"
        else:
            gas_state = "No Gas"
        
            print(
            "Accelerometer data:{} Gyroscope data:{} IRState:{} Gas State:{} Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
               accelerometer_data, gyroscope_data, ir_state, gas_state, temperature_f, temperature_c, humidity
            )
    
        )
        
        data = {
        "Temperature" : temperature_c,
        "Humidity" : humidity,
        "IRState" : ir_state,
        "Gas State" : gas_state,
        "Accelerometer Data" : accelerometer_data,
        "Gyroscope Data" : gyroscope_data
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
    

