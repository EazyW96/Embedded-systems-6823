"""
Sensor Manager Module.

This module is responsible for initializing and managing all sensors,
including the camera, ultrasonic sensor, and BLE module.
It provides a unified interface for retrieving sensor data in real time.
"""
from Ultrasonic import *
ultrasonic = Ultrasonic()
import time 

def test_Ultrasonic():
    try:
        while True:
            data = ultrasonic.get_distance()  #Get the distance value
            print ("Obstacle distance is "+str(data) + "CM")
            time.sleep(1)
    except KeyboardInterrupt:
        print ;"End of Program"

