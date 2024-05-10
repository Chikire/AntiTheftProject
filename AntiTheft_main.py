# 2024 KELVIN OBIOHA

from picamera2 import Picamera2, Preview
import mpu6050
from datetime import datetime
import os
import time
import board
import adafruit_dht
import pyrebase
import RPi.GPIO as GPIO
import secrets
import yagmail


piCam = Picamera2()

# set up the gpio mode
GPIO.setmode(GPIO.BCM)
mpu6050 = mpu6050.mpu6050(0x68)

config = {
    
    #"apiKey": "AIzaSyAYhqDROyB380LEtd-TITQ9mHfERtYtvBI",
    #"authDomain": "security-8b0ed.firebaseapp.com",
    #"databaseURL": "https://security-8b0ed-default-rtdb.firebaseio.com",
    #"projectId": "security-8b0ed",
    #"storageBucket": "security-8b0ed.appspot.com",
    #"messagingSenderId": "51736479216",
    #"appId": "1:51736479216:web:ba970a088263f943178935",
    #"measurementId": "G-5LEMDKCCGW"
    
    
    "apiKey": "AIzaSyBzW-3h3FOAjMD28aePJAMK9rkjVDj2tQ0",
    "authDomain": "real-time-monitoring-sys-23dac.firebaseapp.com",
    "databaseURL": "https://real-time-monitoring-sys-23dac-default-rtdb.firebaseio.com",
    "projectId": "real-time-monitoring-sys-23dac",
    "storageBucket": "real-time-monitoring-sys-23dac.appspot.com",
    "messagingSenderId": "765840115271",
    "appId": "1:765840115271:web:863868feba503736f49362",
    "measurementId": "G-6H1ZM3NGZ2"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()
storage = firebase.storage()

#set up the pin for reading the dO output
DO_PIN = 18
IRPin = 17
buzzer = 21

GPIO.setup(IRPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(DO_PIN, GPIO.IN)
GPIO.setup(buzzer, GPIO.OUT)

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D6)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
dhtDevice = adafruit_dht.DHT11(board.D6, use_pulseio=False)





def send_email():
    password = "mqahcvnfosaeoxpi"
    yag = yagmail.SMTP('antitheft61@gmail.com', password)


    yag.send(to = 'chikireakuibe@gmail.com',
         subject = "INTRUDER",
         contents = "Intruder alert, please check your dashboard!")
print("Email sent")
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
    time.sleep(0.5)
    now = datetime.now()
    name = f'{secrets.token_hex(6)}.jpg'
    #time_captured = '24th April, 2024'
    time_captured = datetime.now() .strftime('%Y-%M-%d %H:%M:%S')
    piCam.capture_file(name)
    print(name+" saved")
    data = {
        'name': name
        }
    timeCaptured = {
        'Readings': time_captured
        }
    
    #dt = now.strftime("%d%m%Y%H:%M:%S")
    #name = dt+".jpg"
    #piCam.capture_file(name)
    time.sleep(1)
    
    db.child('imageTime').push(timeCaptured)
    db.child('upload').push(data)
    storage.child(name).put(name)
    #storage.child(name).put(name)
    print('Image Captured successfully')
    os.remove(name)
    piCam.stop_preview()
    time.sleep(0.5)
    
while True:
    try:
        # Print the values to the serial port
        gyroscope_data = read_sensor_data()
        gx = float(gyroscope_data[0]['x']) + 3.9062228234612113
        temperature_c = dhtDevice.temperature
       # temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        gas_present = GPIO.input(DO_PIN)
        # Read the sensor data
        #gyroscope_data = read_sensor_data()
       # gx = float(gyroscope_data['x']) #+ 3.9062228234612113
       # gy = float(gyroscope_data['y']) + 1.2597942903769574
       # gz = float(gyroscope_data['z']) + 1.270278395121377
        #motion_state = GPIO.input(MOTION_PIN)
        IR_state = GPIO.input(IRPin)
        
        if (IR_state == GPIO.LOW and gx > 4.0000000000000):
            print("true")
            ir_state = "MOTION DETECTED"
            GPIO.output(buzzer, GPIO.HIGH);
            capture_image()
            send_email()
        else:
            ir_state = "NO MOTION"
            GPIO.output(buzzer, GPIO.LOW);
            piCam.stop()
        
        if gas_present == GPIO.LOW:
            gas_state = "Gas Present"
        else:
            gas_state = "No Gas Present"
            print("gx", gx)
        
        #"""data = {
        #"Temperature" : temperature_c,
        #"Humidity" : humidity,
        #"IRState" : ir_state,
        ##"Gas State" : gas_state,
        #"Accelerometer Data" : accelerometer_data,
       # "Gyroscope Data" : gyroscope_data
       # }
        #db.child("Status").push(data)

        #db.update(data)"""
        
        
        
        data1 = {
            'Readings': temperature_c
            }
        data2 = {
            'Readings': humidity
            }
        data3 = {
            'Readings': gas_state
            }
        
        db.child('temperature').push(data1)
        db.child('humidity').push(data2)
        db.child('gas').push(data3)
        print("Sent to Firebase")

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(0.5)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
    #finally:
     #   GPIO.cleanup()
    time.sleep(0.5)
    

