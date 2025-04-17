import asyncio 
import time 
import os
import RPi.GPIO as GPIO
from picamera2 import Picamera2 
from modules.head_movement import HeadMovement 
from modules.motor_control import MotorControl 
from modules.sensor_manager import SensorManager 
 
# ? Your photo save path
PHOTO_DIR = "/home/ciaon/Embedded-systems-6823/ble_images"
os.makedirs(PHOTO_DIR, exist_ok=True)

# ? Your Bluetooth MAC address
TARGET_MAC = "14:1B:A0:17:11:83"
 
async def main(): 
    motor = MotorControl() 
    head = HeadMovement() 
    camera = Picamera2() 
    sensor = SensorManager(target_mac=TARGET_MAC)  # ? Updated to use your MAC

    camera.configure(camera.create_still_configuration()) 
    camera.start() 
    time.sleep(2) 
 
    try: 
        while True: 
            await sensor.react_to_ble_and_take_photo(motor, head, camera, PHOTO_DIR) 
            await asyncio.sleep(1) 
    except KeyboardInterrupt: 
        print("Shutdown.") 
    finally: 
        camera.stop() 
        motor.cleanup() 
        sensor.cleanup_ultrasonic()
        print("Main cleanup...")
        #GPIO.cleanup()
        print("Cleanup done...")
 
if __name__ == "__main__": 
    asyncio.run(main())
