#in this code we tested the gyroscope with the calibrated values from calibration test

import mpu6050
import time
from time import sleep
import RPi.GPIO as GPIO
import board

mpu6050 = mpu6050.mpu6050(0x68)

def read_sensor_data():
    # Read the accelerometer values
    accelerometer_data = mpu6050.get_accel_data()

    # Read the gyroscope values
    gyroscope_data = mpu6050.get_gyro_data()

    # Read temp
    temperature = mpu6050.get_temp()

    return gyroscope_data
    

while True:
    try:
        gyroscope_data = read_sensor_data()
        gx = gyroscope_data['x'] + 3.9062228234612113
        gy = gyroscope_data['y'] + 1.2597942903769574
        gz = gyroscope_data['z'] + 1.2702783951213770
        
        print("gx",gx,"\t","gy",gy,"\t","gz",gz)
        time.sleep(0.2)
        
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("GPIO Good To Go")